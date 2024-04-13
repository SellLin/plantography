import torch
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import AutoencoderKL, DDIMScheduler, DDIMInverseScheduler, DPMSolverMultistepScheduler
from .unet_2d_condition import UNet2DConditionModel
from easydict import EasyDict
import numpy as np
# For compatibility
from utils.latents import get_unscaled_latents, get_scaled_latents, blend_latents
from utils import torch_device
from safetensors.torch import load_file

def load_sd(key="runwayml/stable-diffusion-v1-5", use_fp16=False, load_inverse_scheduler=True):
    """
    Keys:
     key = "CompVis/stable-diffusion-v1-4"
     key = "runwayml/stable-diffusion-v1-5"
     key = "stabilityai/stable-diffusion-2-1-base"
     
    Unpack with:
    ```
    model_dict = load_sd(key=key, use_fp16=use_fp16)
    vae, tokenizer, text_encoder, unet, scheduler, dtype = model_dict.vae, model_dict.tokenizer, model_dict.text_encoder, model_dict.unet, model_dict.scheduler, model_dict.dtype
    ```
    
    use_fp16: fp16 might have degraded performance
    """

    # run final results in fp32
    if use_fp16:
        dtype = torch.float16
        revision = "fp16"
    else:
        dtype = torch.float
        revision = "main"

    vae = AutoencoderKL.from_pretrained(key, subfolder="vae", revision=revision, torch_dtype=dtype).to(torch_device)
    tokenizer = CLIPTokenizer.from_pretrained(key, subfolder="tokenizer", revision=revision, torch_dtype=dtype)
    text_encoder = CLIPTextModel.from_pretrained(key, subfolder="text_encoder", revision=revision, torch_dtype=dtype).to(torch_device)
    unet = UNet2DConditionModel.from_pretrained(key, subfolder="unet", revision=revision, torch_dtype=dtype).to(torch_device)
    dpm_scheduler = DPMSolverMultistepScheduler.from_pretrained(key, subfolder="scheduler", revision=revision, torch_dtype=dtype)
    scheduler = DDIMScheduler.from_pretrained(key, subfolder="scheduler", revision=revision, torch_dtype=dtype)

    # #########################################
    #LORA PATH!!!!!!!

    model_path = "crepen_tulip.safetensors"
    state_dict = load_file(model_path)

    LORA_PREFIX_UNET = 'lora_unet'
    LORA_PREFIX_TEXT_ENCODER = 'lora_te'

    alpha = 0.8

    visited = []
    # directly update weight in diffusers model
    for kiss in state_dict:

        # it is suggested to print out the key, it usually will be something like below
        # "lora_te_text_model_encoder_layers_0_self_attn_k_proj.lora_down.weight"

        # as we have set the alpha beforehand, so just skip
        if '.alpha' in kiss or kiss in visited:
            continue

        if 'text' in kiss:
            layer_infos = kiss.split('.')[0].split(LORA_PREFIX_TEXT_ENCODER + '_')[-1].split('_')
            curr_layer = text_encoder
        else:
            layer_infos = kiss.split('.')[0].split(LORA_PREFIX_UNET + '_')[-1].split('_')
            curr_layer = unet

        # find the target layer
        temp_name = layer_infos.pop(0)
        while len(layer_infos) > -1:
            try:
                curr_layer = curr_layer.__getattr__(temp_name)
                if len(layer_infos) > 0:
                    temp_name = layer_infos.pop(0)
                elif len(layer_infos) == 0:
                    break
            except Exception:
                if len(temp_name) > 0:
                    temp_name += '_' + layer_infos.pop(0)
                else:
                    temp_name = layer_infos.pop(0)

        # org_forward(x) + lora_up(lora_down(x)) * multiplier
        pair_keys = []
        if 'lora_down' in kiss:
            pair_keys.append(kiss.replace('lora_down', 'lora_up'))
            pair_keys.append(kiss)
        else:
            pair_keys.append(kiss)
            pair_keys.append(kiss.replace('lora_up', 'lora_down'))

        # update weight
        if len(state_dict[pair_keys[0]].shape) == 4:
            weight_up = state_dict[pair_keys[0]].squeeze(3).squeeze(2).to(torch.float32)
            weight_down = state_dict[pair_keys[1]].squeeze(3).squeeze(2).to(torch.float32)
            curr_layer.weight.data += alpha * torch.mm(weight_up, weight_down).unsqueeze(2).unsqueeze(3).to(torch_device)
        else:
            weight_up = state_dict[pair_keys[0]].to(torch.float32)
            weight_down = state_dict[pair_keys[1]].to(torch.float32)
            curr_layer.weight.data += alpha * torch.mm(weight_up, weight_down).to(torch_device)

        # update visited list
        for item in pair_keys:
            visited.append(item)

    model_dict = EasyDict(vae=vae, tokenizer=tokenizer, text_encoder=text_encoder, unet=unet, scheduler=scheduler, dpm_scheduler=dpm_scheduler, dtype=dtype)

    if load_inverse_scheduler:
        inverse_scheduler = DDIMInverseScheduler.from_config(scheduler.config)
        model_dict.inverse_scheduler = inverse_scheduler

    return model_dict

def encode_prompts(tokenizer, text_encoder, prompts, negative_prompt="", return_full_only=False, one_uncond_input_only=False):
    if negative_prompt == "":
        print("Note that negative_prompt is an empty string")

    text_input = tokenizer(
        prompts, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt"
    )

    max_length = text_input.input_ids.shape[-1]
    if one_uncond_input_only:
        num_uncond_input = 1
    else:
        num_uncond_input = len(prompts)
    uncond_input = tokenizer([negative_prompt] * num_uncond_input, padding="max_length", max_length=max_length, return_tensors="pt")

    with torch.no_grad():
        uncond_embeddings = text_encoder(uncond_input.input_ids.to(torch_device))[0]
        cond_embeddings = text_encoder(text_input.input_ids.to(torch_device))[0]

    if one_uncond_input_only:
        return uncond_embeddings, cond_embeddings

    text_embeddings = torch.cat([uncond_embeddings, cond_embeddings])

    if return_full_only:
        return text_embeddings
    return text_embeddings, uncond_embeddings, cond_embeddings

def process_input_embeddings(input_embeddings):
    assert isinstance(input_embeddings, (tuple, list))
    if len(input_embeddings) == 3:
        # input_embeddings: text_embeddings, uncond_embeddings, cond_embeddings
        # Assume `uncond_embeddings` is full (has batch size the same as cond_embeddings)
        _, uncond_embeddings, cond_embeddings = input_embeddings
        assert uncond_embeddings.shape[0] == cond_embeddings.shape[0], f"{uncond_embeddings.shape[0]} != {cond_embeddings.shape[0]}"
        return input_embeddings
    elif len(input_embeddings) == 2:
        # input_embeddings: uncond_embeddings, cond_embeddings
        # uncond_embeddings may have only one item
        uncond_embeddings, cond_embeddings = input_embeddings
        if uncond_embeddings.shape[0] == 1:
            uncond_embeddings = uncond_embeddings.expand(cond_embeddings.shape)
        # We follow the convention: negative (unconditional) prompt comes first
        text_embeddings = torch.cat((uncond_embeddings, cond_embeddings), dim=0)
        return text_embeddings, uncond_embeddings, cond_embeddings
    else:
        raise ValueError(f"input_embeddings length: {len(input_embeddings)}")
