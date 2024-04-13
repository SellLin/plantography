import gradio as gr
import numpy as np
import os
import matplotlib.pyplot as plt
from utils.parse import filter_boxes, parse_input_with_negative, show_boxes
from generation import run as run_ours
from generation import run_in_batch
from baseline import run as run_baseline
import torch
from shared import DEFAULT_SO_NEGATIVE_PROMPT, DEFAULT_OVERALL_NEGATIVE_PROMPT
from examples import stage1_examples, stage2_examples, default_template, simplified_prompt, prompt_placeholder, layout_placeholder

cuda_available = torch.cuda.is_available()

print(f"Is CUDA available: {torch.cuda.is_available()}")

if cuda_available:
    gpu_memory = torch.cuda.get_device_properties(torch.cuda.current_device()).total_memory
    low_memory = gpu_memory <= 16 * 1024 ** 3
    print(f"CUDA device: {torch.cuda.get_device_name(torch.cuda.current_device())}. With GPU memory: {gpu_memory}. Low memory: {low_memory}")
else:
    low_memory = False

cache_examples = True
default_num_inference_steps = 20 if low_memory else 50

def get_lmd_prompt(prompt, template=default_template):
    if prompt == "":
        prompt = prompt_placeholder
    if template == "":
        template = default_template
    return simplified_prompt.format(template=template, prompt=prompt)

def get_layout_image(response):
    if response == "":
        response = layout_placeholder
    gen_boxes, bg_prompt, neg_prompt = parse_input_with_negative(response, no_input=True)
    fig = plt.figure(figsize=(8, 8))
    # https://stackoverflow.com/questions/7821518/save-plot-to-numpy-array
    show_boxes(gen_boxes, bg_prompt, neg_prompt)
    # If we haven't already shown or saved the plot, then we need to
    # draw the figure first...
    fig.canvas.draw()

    # Now we can save it to a numpy array.
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.clf()
    return data

def get_layout_image_gallery(response):
    return [get_layout_image(response)]

def get_ours_image(response, overall_prompt_override="", seed=0, num_inference_steps=250, dpm_scheduler=True, use_autocast=False, fg_seed_start=20, fg_blending_ratio=0.1, frozen_step_ratio=0.5, attn_guidance_step_ratio=0.6, gligen_scheduled_sampling_beta=0.4, attn_guidance_scale=20, use_ref_ca=True, so_negative_prompt=DEFAULT_SO_NEGATIVE_PROMPT, overall_negative_prompt=DEFAULT_OVERALL_NEGATIVE_PROMPT, show_so_imgs=False, scale_boxes=False):
    if response == "":
        if overall_prompt_override == "":
            # Both are empty so generate a placeholder
            response = layout_placeholder
        else:
            raise gr.Error("You entered a prompt for overall image but left the ChatGPT response empty. Please paste ChatGPT response or select an example below to get started.")
    gen_boxes, bg_prompt, neg_prompt = parse_input_with_negative(response, no_input=True)
    gen_boxes = filter_boxes(gen_boxes, scale_boxes=scale_boxes)
    spec = {
        # prompt is unused
        'prompt': '',
        'gen_boxes': gen_boxes,
        'bg_prompt': bg_prompt, 
        'extra_neg_prompt': neg_prompt
    }
    
    if dpm_scheduler:
        scheduler_key = "dpm_scheduler"
    else:
        scheduler_key = "scheduler"
    
    overall_max_index_step = int(attn_guidance_step_ratio * num_inference_steps)

    image_np, so_img_list = run_ours(
        spec, bg_seed=seed, overall_prompt_override=overall_prompt_override, fg_seed_start=fg_seed_start,
        fg_blending_ratio=fg_blending_ratio,frozen_step_ratio=frozen_step_ratio, use_autocast=use_autocast,
        so_gligen_scheduled_sampling_beta=gligen_scheduled_sampling_beta, overall_gligen_scheduled_sampling_beta=gligen_scheduled_sampling_beta, num_inference_steps=num_inference_steps, scheduler_key=scheduler_key,
        use_ref_ca=use_ref_ca, so_negative_prompt=so_negative_prompt, overall_negative_prompt=overall_negative_prompt,
        loss_scale=attn_guidance_scale, max_index_step=0, overall_loss_scale=attn_guidance_scale, overall_max_index_step=overall_max_index_step,
    )
    '''
     # test run in batch
    image_np, so_img_list = run_in_batch(
     spec, bg_seed=seed, overall_prompt_override=overall_prompt_override, fg_seed_start=fg_seed_start,
     fg_blending_ratio=fg_blending_ratio,frozen_step_ratio=frozen_step_ratio, use_autocast=use_autocast,
     so_gligen_scheduled_sampling_beta=gligen_scheduled_sampling_beta, overall_gligen_scheduled_sampling_beta=gligen_scheduled_sampling_beta, num_inference_steps=num_inference_steps, scheduler_key=scheduler_key,
     use_ref_ca=use_ref_ca, so_negative_prompt=so_negative_prompt, overall_negative_prompt=overall_negative_prompt,
     loss_scale=attn_guidance_scale, max_index_step=0, overall_loss_scale=attn_guidance_scale, overall_max_index_step=overall_max_index_step,batch_size = 200
    )
    '''

    images = [image_np]
    if show_so_imgs:
        images.extend([np.asarray(so_img) for so_img in so_img_list])
    
    if cuda_available:
        print(f"Max GPU memory allocated: {torch.cuda.max_memory_allocated() / 1024 ** 3:.2f} GB")
        torch.cuda.reset_max_memory_allocated()
    
    return images

def get_baseline_image(prompt, seed=0):
    if prompt == "":
        prompt = prompt_placeholder
    
    scheduler_key = "dpm_scheduler"
    num_inference_steps = 20
    
    image_np = run_baseline(prompt, bg_seed=seed, scheduler_key=scheduler_key, num_inference_steps=num_inference_steps)
    return [image_np]

duplicate_html = '<a style="display:inline-block" href="https://huggingface.co/spaces/longlian/llm-grounded-diffusion?duplicate=true"><img src="https://img.shields.io/badge/-Duplicate%20Space-blue?labelColor=white&style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAP5JREFUOE+lk7FqAkEURY+ltunEgFXS2sZGIbXfEPdLlnxJyDdYB62sbbUKpLbVNhyYFzbrrA74YJlh9r079973psed0cvUD4A+4HoCjsA85X0Dfn/RBLBgBDxnQPfAEJgBY+A9gALA4tcbamSzS4xq4FOQAJgCDwV2CPKV8tZAJcAjMMkUe1vX+U+SMhfAJEHasQIWmXNN3abzDwHUrgcRGmYcgKe0bxrblHEB4E/pndMazNpSZGcsZdBlYJcEL9Afo75molJyM2FxmPgmgPqlWNLGfwZGG6UiyEvLzHYDmoPkDDiNm9JR9uboiONcBXrpY1qmgs21x1QwyZcpvxt9NS09PlsPAAAAAElFTkSuQmCC&logoWidth=14" alt="Duplicate Space"></a>'

html = f"""<h1>LLM-grounded Diffusion: Enhancing Prompt Understanding of Text-to-Image Diffusion Models with Large Language Models</h1>
            <h2>LLM + Stable Diffusion => better prompt understanding in text2image generation 🤩</h2>
            <h2><a href='https://llm-grounded-diffusion.github.io/'>Project Page</a> | <a href='https://bair.berkeley.edu/blog/2023/05/23/lmd/'>5-minute Blog Post</a> | <a href='https://arxiv.org/pdf/2305.13655.pdf'>ArXiv Paper</a> | <a href='https://github.com/TonyLianLong/LLM-groundedDiffusion'>Github</a> | <a href='https://llm-grounded-diffusion.github.io/#citation'>Cite our work</a> if our ideas inspire you.</h2>
            <p><b>Try some examples at the bottom of the page to get started!</b></p>
            <p><b>Tips:</b></p>
            <p>1. If ChatGPT doesn't generate layout, add/remove the trailing space (added by default) and/or use GPT-4.</p>
            <p>2. You can perform multi-round specification by giving ChatGPT follow-up requests (e.g., make the objects bigger or move the objects).</p>
            <p>3. You can also try prompts in Simplified Chinese. You need to leave "prompt for overall image" empty in this case. If you want to try prompts in another language, translate the first line of last example to your language.</p>
            <p>4. The diffusion model only runs {default_num_inference_steps} steps by default in this demo. You can make it run more steps to get higher quality images (or tweak frozen steps/guidance steps for better guidance and coherence).</p>
            <p>5. Duplicate this space and add GPU or clone the space and run locally to skip the queue and run our model faster. (<b>Currently we are using a T4 GPU on this space, which is quite slow, and you can add a A10G to make it 5x faster</b>) {duplicate_html}</p>
            <br/>
            <p>An implementation note (updated): In this demo, we provide a few modes: faster generation by disabling attention/per-box guidance. The standard version describes what is implemented for the paper. You can also set GLIGEN guidance steps ratio to 0 to disable GLIGEN and to see what you get with only the original SD weights.</p>
            <style>.btn {{flex-grow: unset !important;}} </p>
            """

def preset_change(preset):
    # frozen_step_ratio, attn_guidance_step_ratio, attn_guidance_scale, use_ref_ca, so_negative_prompt
    if preset == "Standard":
        return gr.update(value=0.5, interactive=True), gr.update(value=0.6, interactive=True), gr.update(interactive=True), gr.update(value=True, interactive=True), gr.update(interactive=True)
    elif preset == "Faster (disable attention guidance, keep per-box guidance)":
        return gr.update(value=0.5, interactive=True), gr.update(value=0, interactive=False), gr.update(interactive=False), gr.update(value=True, interactive=True), gr.update(interactive=True)
    elif preset == "Faster (disable per-box guidance, keep attention guidance)":
        return gr.update(value=0, interactive=False), gr.update(value=0.6, interactive=True), gr.update(interactive=True), gr.update(value=False, interactive=False), gr.update(interactive=False)
    elif preset == "Fastest (disable both)":
        return gr.update(value=0, interactive=False), gr.update(value=0, interactive=False), gr.update(interactive=False), gr.update(value=False, interactive=False), gr.update(interactive=True)
    else:
        raise gr.Error(f"Unknown preset {preset}")

with gr.Blocks(
    title="LLM-grounded Diffusion: Enhancing Prompt Understanding of Text-to-Image Diffusion Models with Large Language Models"
) as g:
    gr.HTML(html)
    with gr.Tab("Stage 1. Image Prompt to ChatGPT"):
        with gr.Row():
            with gr.Column(scale=1):
                prompt = gr.Textbox(lines=2, label="Prompt for Layout Generation", placeholder=prompt_placeholder)
                generate_btn = gr.Button("Generate Prompt", variant='primary', elem_classes="btn")
                with gr.Accordion("Advanced options", open=False):
                    template = gr.Textbox(lines=10, label="Custom Template", placeholder="Customized Template", value=default_template)
            with gr.Column(scale=1):
                output = gr.Textbox(label="Paste this into ChatGPT (GPT-4 preferred; on Mac, click text and press Command+A and Command+C to copy all)", show_copy_button=True)
                gr.HTML("<a href='https://chat.openai.com' target='_blank'>Click here to open ChatGPT</a>")
        generate_btn.click(fn=get_lmd_prompt, inputs=[prompt, template], outputs=output, api_name="get_lmd_prompt")
    
        gr.Examples(
            examples=stage1_examples,
            inputs=[prompt],
            outputs=[output],
            fn=get_lmd_prompt,
            cache_examples=cache_examples,
            label="Examples"
        )
    
    with gr.Tab("Stage 2 (New). Layout to Image generation"):
        with gr.Row():
            with gr.Column(scale=1):
                overall_prompt_override = gr.Textbox(lines=2, label="Prompt for the overall image (optional but recommended)", placeholder="You can put your input prompt for layout generation here, helpful if your scene cannot be represented by background prompt and boxes only, e.g., with object interactions. If left empty, we will use: background prompt with [objects].", value="")
                response = gr.Textbox(lines=8, label="Paste ChatGPT response here (no original caption needed here)", placeholder="Get started with some examples at the bottom of the page. If left empty, we will use the following: \n\n" + layout_placeholder)
                num_inference_steps = gr.Slider(1, 100 if low_memory else 250, value=default_num_inference_steps, step=1, label="Number of denoising steps (set to >=50 for higher generation quality)")
                # Using a environment variable allows setting default to faster/fastest on low-end GPUs.
                preset = gr.Radio(label="Guidance: apply less control for faster generation", choices=["Standard", "Faster (disable attention guidance, keep per-box guidance)", "Faster (disable per-box guidance, keep attention guidance)", "Fastest (disable both)"], value="Faster (disable attention guidance, keep per-box guidance)" if low_memory else "Standard")
                seed = gr.Slider(0, 10000, value=0, step=1, label="Seed")
                with gr.Accordion("Advanced options (play around for better generation)", open=False):
                    with gr.Tab("Guidance"):
                        frozen_step_ratio = gr.Slider(0, 1, value=0.5, step=0.1, label="Foreground frozen steps ratio (higher: stronger attribute binding; lower: higher coherence")
                        gligen_scheduled_sampling_beta = gr.Slider(0, 1, value=0.4, step=0.1, label="GLIGEN guidance steps ratio (the beta value, higher: stronger GLIGEN guidance)")
                        # Since the default mode is "Faster (disable attention guidance, keep per-box guidance)" if `low_memory`, we disable attention guidance here if `low_memory` by default to match the preset and they can be enabled if the user selects another preset.
                        attn_guidance_step_ratio = gr.Slider(0, 1, value=0.6 if not low_memory else 0, step=0.01, label="Attention guidance steps ratio (higher: stronger attention guidance; lower: faster and higher coherence", interactive=not low_memory)
                        attn_guidance_scale = gr.Slider(0, 50, value=20, step=0.5, label="Attention guidance scale: 0 means no attention guidance.", interactive=not low_memory)
                        use_ref_ca = gr.Checkbox(label="Using per-box attention to guide reference attention", show_label=False, value=True)
                    with gr.Tab("Generation"):
                        dpm_scheduler = gr.Checkbox(label="Use DPM scheduler (unchecked: DDIM scheduler, may have better coherence, recommend >=50 inference steps)", show_label=False, value=True)
                        use_autocast = gr.Checkbox(label="Use FP16 Mixed Precision (faster but with slightly lower quality)" + " [enabled due to low GPU memory]" if low_memory else "", show_label=False, value=True, interactive=not low_memory)
                        fg_seed_start = gr.Slider(0, 10000, value=20, step=1, label="Seed for foreground variation")
                        fg_blending_ratio = gr.Slider(0, 1, value=0.1, step=0.01, label="Variations added to foreground for single object generation (0: no variation, 1: max variation)")
                        scale_boxes = gr.Checkbox(label="Scale bounding boxes to just fit the scene", show_label=False, value=False)
                        so_negative_prompt = gr.Textbox(lines=1, label="Negative prompt for single object generation", value=DEFAULT_SO_NEGATIVE_PROMPT)
                        overall_negative_prompt = gr.Textbox(lines=1, label="Negative prompt for overall generation", value=DEFAULT_OVERALL_NEGATIVE_PROMPT)
                        show_so_imgs = gr.Checkbox(label="Show annotated single object generations", show_label=False, value=False)
                visualize_btn = gr.Button("Visualize Layout", elem_classes="btn")
                generate_btn = gr.Button("Generate Image from Layout", variant='primary', elem_classes="btn")
            with gr.Column(scale=1):
                gallery = gr.Gallery(
                    label="Generated image", show_label=False, elem_id="gallery", columns=[1], rows=[1], object_fit="contain", preview=True
                )
        preset.change(preset_change, [preset], [frozen_step_ratio, attn_guidance_step_ratio, attn_guidance_scale, use_ref_ca, so_negative_prompt])
        prompt.change(None, [prompt], overall_prompt_override, _js="(x) => x")
        visualize_btn.click(fn=get_layout_image_gallery, inputs=response, outputs=gallery, api_name="visualize-layout")
        generate_btn.click(fn=get_ours_image, inputs=[response, overall_prompt_override, seed, num_inference_steps, dpm_scheduler, use_autocast, fg_seed_start, fg_blending_ratio, frozen_step_ratio, attn_guidance_step_ratio, gligen_scheduled_sampling_beta, attn_guidance_scale, use_ref_ca, so_negative_prompt, overall_negative_prompt, show_so_imgs, scale_boxes], outputs=gallery, api_name="layout-to-image")

        gr.Examples(
            examples=stage2_examples,
            inputs=[response, overall_prompt_override, seed],
            outputs=[gallery],
            fn=get_ours_image,
            cache_examples=cache_examples,
            label="Examples"
        )

    with gr.Tab("Baseline: Stable Diffusion"):
        with gr.Row():
            with gr.Column(scale=1):
                sd_prompt = gr.Textbox(lines=2, label="Prompt for baseline SD", placeholder=prompt_placeholder)
                seed = gr.Slider(0, 10000, value=0, step=1, label="Seed")
                generate_btn = gr.Button("Generate", elem_classes="btn")

            with gr.Column(scale=1):
                gallery = gr.Gallery(
                    label="Generated image", show_label=False, elem_id="gallery2", columns=[1], rows=[1], object_fit="contain", preview=True
                )
        generate_btn.click(fn=get_baseline_image, inputs=[sd_prompt, seed], outputs=gallery, api_name="baseline")

        gr.Examples(
            examples=stage1_examples,
            inputs=[sd_prompt],
            outputs=[gallery],
            fn=get_baseline_image,
            cache_examples=cache_examples,
            label="Examples"
        )

g.launch()
