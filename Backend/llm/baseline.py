# Original Stable Diffusion (1.4)

import torch
import models
from models import pipelines
from shared import model_dict, DEFAULT_OVERALL_NEGATIVE_PROMPT
import gc

vae, tokenizer, text_encoder, unet, scheduler, dtype = model_dict.vae, model_dict.tokenizer, model_dict.text_encoder, model_dict.unet, model_dict.scheduler, model_dict.dtype

torch.set_grad_enabled(False)

height = 512  # default height of Stable Diffusion
width = 512  # default width of Stable Diffusion
guidance_scale = 7.5  # Scale for classifier-free guidance
batch_size = 1

# h, w
image_scale = (512, 512)

bg_negative = DEFAULT_OVERALL_NEGATIVE_PROMPT

# Using dpm scheduler by default
def run(prompt, scheduler_key='dpm_scheduler', bg_seed=1, num_inference_steps=20):
    print(f"prompt: {prompt}")
    generator = torch.manual_seed(bg_seed)
    
    prompts = [prompt]
    input_embeddings = models.encode_prompts(prompts=prompts, tokenizer=tokenizer, text_encoder=text_encoder, negative_prompt=bg_negative)

    latents = models.get_unscaled_latents(batch_size, unet.config.in_channels, height, width, generator, dtype)

    latents = latents * scheduler.init_noise_sigma

    pipelines.gligen_enable_fuser(model_dict['unet'], enabled=False)
    _, images = pipelines.generate(
        model_dict, latents, input_embeddings, num_inference_steps,  
        guidance_scale=guidance_scale, scheduler_key=scheduler_key
    )
    
    gc.collect()
    torch.cuda.empty_cache()

    return images[0]



if True:
    import os
    from PIL import Image
    import numpy as np
    folder_path = "C:/Users/user/PycharmProjects/landscapeDesign/llm-grounded-diffusion/batch_result/questionnaire_text_image/Text_Prompt_Alightment/Ours"
    out_folder_path = "C:/Users/user/PycharmProjects/landscapeDesign/llm-grounded-diffusion/batch_result/questionnaire_text_image/Text_Prompt_Alightment/Generate"
    out_path_9_8 = "C:/Users/user/PycharmProjects/landscapeDesign/llm-grounded-diffusion/batch_result/9_8"
    p = {
        "banya": {"t": 1, "n": "Banyaugs"},
        "weep": {"t": 1, "n": "Weepingwillowshr"},
        "dogwood": {"t": 1, "n": "Dogwoodxyz"},
        "jap": {"t": 1, "n": "japanesepinexyz"},
        "crepen": {"t": 1, "n": "crapemyrtlexyz"},

        "lily": {"t": 2, "n": "Africanlilyxyz"},
        "tulip": {"t": 2, "n": "Whitetulipgur"},
    }

    def get_promps(plans):
        if len(plans) == 1:
            if plans[0]["t"] == 1:
                return "Beautiful scenery. A realistic photo of a {} in a park. blue sky. Sunset, grass, cloud.".format(
                    plans[0]["n"])
            else:
                return "Beautiful scenery. A realistic photo of a {} in front of a river in the park with blue sky. Sunset, grass, cloud.".format(
                    plans[0]["n"])
        elif len(plans) == 2:
            if plans[1]["t"] == 1:
                return "Beautiful scenery. A realistic photo of a {} and a {} in a park. blue sky. Sunset, grass, cloud.".format(
                    plans[0]["n"], plans[1]["n"])
            else:
                return "Beautiful scenery. A realistic photo of a {} in front of a river and a {} in front of a {} in the park with blue sky. Sunset, grass, cloud.".format(
                    plans[0]["n"], plans[1]["n"], plans[0]["n"])

    p_dic = {'weep_two_tree': [p["weep"], p["weep"]],
             'crepen_two_tree': [p["crepen"], p["crepen"]],
             'Banya_two_tree': [p["banya"], p["banya"]],
             'weep_jap': [p["weep"], p["jap"]],
             'crepen_alone': [p["crepen"]],
             'Banya_lily': [p["banya"], p["lily"]],
             'dogwood_weep': [p["dogwood"], p["weep"]],
             'dogwood+lily': [p["dogwood"], p["lily"]],
             'Banya_jap': [p["banya"], p["jap"]],
             'weep_alone': [p["weep"]],
             'dogwood_alone': [p["dogwood"]],
             'dogwood_two_tree': [p["dogwood"], p["dogwood"]],
             'jap_two_tree': [p["jap"], p["jap"]],
             'jap_lily': [p["jap"], p["lily"]],
             'Banya_tulip': [p["banya"], p["tulip"]],
             'Tulip': [p["tulip"]],
             'weep_tulip': [p["weep"], p["tulip"]],
             'dogwood_jap': [p["dogwood"], p["jap"]],
             'jap_tulip': [p["jap"], p["tulip"]],
             'Banya_alone': [p["banya"]],
             'lily': [p["lily"]],
             'weep+banya': [p["weep"], p["banya"]],
             'dogwood_tulip': [p["dogwood"], p["tulip"]],
             'jap_alone': [p["jap"]]}
    p1 = []
    p2 = []
    for item in p_dic:
        flag = True
        filename = item
        modes = [p["dogwood"], p["lily"]]
        for i in p_dic[filename]:
            if i not in modes:
                flag = False
        if flag:
            if not os.path.exists(out_path_9_8 + "/" + filename + "__base"):
                os.makedirs(out_path_9_8 + "/" + filename + "__base")
            else:
                continue
            for j in range(1241, 1442):
                num = j
                img = run(get_promps(p_dic[filename]), bg_seed=int(num))
                Image.fromarray(img).save(out_path_9_8 + "/" + filename + "__base" + "/image_{}_{}.png".format(filename, num), "png")

    # flag = True
        # flag2 = True
        # p1.append(filename.split("__")[-2])
        # p2.append(filename.split("__")[-1])
        #
        # # modes = [p["crepen"], p["banya"], p["weep"], p["lily"]]
        # modes = [p["weep"], p["tulip"]]
        # p11 = p_dic[filename.split("__")[-2]]
        # p22 = p_dic[filename.split("__")[-1]]
        # for i in p11:
        #     if i not in modes:
        #         flag = False
        # if flag:
        #     for file in os.listdir("data/" + filename):
        #         num = file.split("_")[-1].split(".")[0]
        #         img = run(get_promps(p11), bg_seed=int(num))
        #         Image.fromarray(img).save(folder_path + "/" + filename + "/3_{}.png".format(num), "png")
        #
        # for j in p22:
        #     if j not in modes:
        #         flag2 = False
        # if flag2:
        #     for file in os.listdir("data/" + filename):
        #         num = file.split("_")[-1].split(".")[0]
        #         img = run(get_promps(p22), bg_seed=int(num))
        #         Image.fromarray(img).save(folder_path + "/" + filename + "/4_{}.png".format(num), "png")



"""
if True:
    print("11111")
    import os
    from PIL import Image
    import numpy as np
    folder_path = "C:/Users/user/PycharmProjects/landscapeDesign/llm/batch_result/questionnaire_text_image/Text_Prompt_Alightment/Ours"
    out_folder_path = "C:/Users/user/PycharmProjects/landscapeDesign/llm/batch_result/questionnaire_text_image/Text_Prompt_Alightment/Generate"
    p = {
        "banya": {"t": 1, "n": "Banya"},
        "weep": {"t": 1, "n": "Weepingwillow"},
        "dogwood": {"t": 1, "n": "Dogwood"},
        "jap": {"t": 1, "n": "japanesepine"},
        "crepen": {"t": 1, "n": "crapemyrtle"},

        "lily": {"t": 2, "n": "Africanlily"},
        "tulip": {"t": 2, "n": "Whitetulip"},
    }

    def get_promps(plans):
        if len(plans) == 1:
            if plans[0]["t"] == 1:
                return "Beautiful scenery. A realistic photo of a {} in a park. blue sky. Sunset, grass, cloud.".format(
                    plans[0]["n"])
            else:
                return "Beautiful scenery. A realistic photo of a {} in front of a river in the park with blue sky. Sunset, grass, cloud.".format(
                    plans[0]["n"])
        elif len(plans) == 2:
            if plans[1]["t"] == 1:
                return "Beautiful scenery. A realistic photo of a {} and a {} in a park. blue sky. Sunset, grass, cloud.".format(
                    plans[0]["n"], plans[1]["n"])
            else:
                return "Beautiful scenery. A realistic photo of a {} in front of a river and a {} in front of a {} in the park with blue sky. Sunset, grass, cloud.".format(
                    plans[0]["n"], plans[1]["n"], plans[0]["n"])

    p_dic = {'tulip': [p["tulip"]],
             'dogwood_weep': [p["dogwood"], p["weep"]],
             'weep_two': [p["weep"], p["weep"]],
             'dogwood_tulip': [p["dogwood"], p["tulip"]],
             'crepen_alone': [p["crepen"]],
             'jap_tulip': [p["jap"], p["tulip"]],
             'Weep_Banya': [p["weep"], p["banya"]],
             'Banya_jap': [p["banya"], p["jap"]],
             'dogwood_alone': [p["dogwood"]],
             'weep_tulip': [p["weep"], p["tulip"]],
             'Banya_tulip': [p["banya"], p["tulip"]],
             'weep_alone': [p["weep"]],
             'dogwood_lily': [p["dogwood"], p["lily"]],
             'jap_lily': [p["jap"], p["lily"]],
             'banya_alone': [p["banya"]],
             'banya_two': [p["banya"], p["banya"]],
             'weep_jap': [p["weep"], p["jap"]],
             'dogwood_two': [p["dogwood"], p["dogwood"]],
             'dogwood_jap': [p["dogwood"], p["jap"]],
             'banya_lily': [p["banya"], p["lily"]],
             'lily': [p["lily"]],
             'jap_two': [p["jap"], p["jap"]],
             'Tulip': [p["tulip"]],
             'Banya_alone': [p["banya"]],
             'weep+banya': [p["weep"], p["banya"]],
             'jap_alone': [p["jap"]]}
    p1 = []
    for filename in os.listdir(folder_path):
        flag = True
        name = filename.replace("image_", "").replace(".png", "")
        slc = name.split("_")
        name = "_".join(slc[:-1])
        p1.append(name)
        num = slc[-1]
        print(p_dic[name])
        # modes = [p["crepen"], p["banya"], p["weep"], p["lily"]]
        modes = [p["weep"], p["tulip"]]
        img = run(get_promps(p_dic[name]), bg_seed=int(num))
        Image.fromarray(img).save(out_folder_path + "/" + filename, "png")
    print(set(p1))











    if True:
        print("11111")
        import os
        from PIL import Image
        import numpy as np
        folder_path = "C:/Users/user/PycharmProjects/landscapeDesign/llm/data"
        p = {
            "banya": {"t": 1, "n": "Banyaugs"},
            "weep": {"t": 1, "n": "Weepingwillowshr"},
            "dogwood": {"t": 1, "n": "Dogwoodxyz"},
            "jap": {"t": 1, "n": "japanesepinexyz"},
            "crepen": {"t": 1, "n": "crapemyrtlexyz"},
    
            "lily": {"t": 2, "n": "Africanlilyxyz"},
            "tulip": {"t": 2, "n": "Whitetulipgur"},
        }
    
    
        def get_promps(plans):
            if len(plans) == 1:
                if plans[0]["t"] == 1:
                    return "Beautiful scenery. A realistic photo of a {} in a park. blue sky. Sunset, grass, cloud.".format(
                        plans[0]["n"])
                else:
                    return "Beautiful scenery. A realistic photo of a {} in front of a river in the park with blue sky. Sunset, grass, cloud.".format(
                        plans[0]["n"])
            elif len(plans) == 2:
                if plans[1]["t"] == 1:
                    return "Beautiful scenery. A realistic photo of a {} and a {} in a park. blue sky. Sunset, grass, cloud.".format(
                        plans[0]["n"], plans[1]["n"])
                else:
                    return "Beautiful scenery. A realistic photo of a {} in front of a river and a {} in front of a {} in the park with blue sky. Sunset, grass, cloud.".format(
                        plans[0]["n"], plans[1]["n"], plans[0]["n"])
    
    
        p_dic = {'weep_two_tree': [p["weep"], p["weep"]],
                 'crepen_two_tree': [p["crepen"], p["crepen"]],
                 'Banya_two_tree': [p["banya"], p["banya"]],
                 'weep_jap': [p["weep"], p["jap"]],
                 'crepen_alone': [p["crepen"]],
                 'Banya_lily': [p["banya"], p["lily"]],
                 'dogwood_weep': [p["dogwood"], p["weep"]],
                 'dogwood+lily': [p["dogwood"], p["lily"]],
                 'Banya_jap': [p["banya"], p["jap"]],
                 'weep_alone': [p["weep"]],
                 'dogwood_alone': [p["dogwood"]],
                 'dogwood_two_tree': [p["dogwood"], p["dogwood"]],
                 'jap_two_tree': [p["jap"], p["jap"]],
                 'jap_lily': [p["jap"], p["lily"]],
                 'Banya_tulip': [p["banya"], p["tulip"]],
                 'Tulip': [p["tulip"]],
                 'weep_tulip': [p["weep"], p["tulip"]],
                 'dogwood_jap': [p["dogwood"], p["jap"]],
                 'jap_tulip': [p["jap"], p["tulip"]],
                 'Banya_alone': [p["banya"]],
                 'lily': [p["lily"]],
                 'weep+banya': [p["weep"], p["banya"]],
                 'dogwood_tulip': [p["dogwood"], p["tulip"]],
                 'jap_alone': [p["jap"]]}
    
        p1 = []
        p2 = []
        for filename in os.listdir(folder_path):
            flag = True
            flag2 = True
            p1.append(filename.split("__")[-2])
            p2.append(filename.split("__")[-1])
    
            # modes = [p["crepen"], p["banya"], p["weep"], p["lily"]]
            modes = [p["weep"], p["tulip"]]
            p11 = p_dic[filename.split("__")[-2]]
            p22 = p_dic[filename.split("__")[-1]]
            for i in p11:
                if i not in modes:
                    flag = False
            if flag:
                for file in os.listdir("data/" + filename):
                    num = file.split("_")[-1].split(".")[0]
                    img = run(get_promps(p11), bg_seed=int(num))
                    Image.fromarray(img).save(folder_path + "/" + filename + "/3_{}.png".format(num), "png")
    
            for j in p22:
                if j not in modes:
                    flag2 = False
            if flag2:
                for file in os.listdir("data/" + filename):
                    num = file.split("_")[-1].split(".")[0]
                    img = run(get_promps(p22), bg_seed=int(num))
                    Image.fromarray(img).save(folder_path + "/" + filename + "/4_{}.png".format(num), "png")
"""