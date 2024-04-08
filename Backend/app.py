import json
import os
import tempfile
from ast import literal_eval
from datetime import datetime
from threading import Thread

import cv2
import numpy as np
import openai
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from matplotlib import pyplot as plt
from matplotlib.collections import PatchCollection
# from matplotlib import pyplot as plt
# from matplotlib.collections import PatchCollection
from sympy import Polygon

from Backend.default_prompt import get_default_scene_graph
from Backend.llm.generation import run as run_ours
from shared import DEFAULT_SO_NEGATIVE_PROMPT, DEFAULT_OVERALL_NEGATIVE_PROMPT

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# import js

messages = []


openai.api_base = ''
my_api_key = ''
openai.api_key = my_api_key

app = Flask(__name__)
FILE_ABS_PATH = os.path.dirname(__file__)
CORS(app)

# global variables
background_prompts = ['']
timer = [0]


def get_prompt_caption(path):
    default_caption, default_scene_graph = get_default_scene_graph(path)
    scene_graph_format = """"{objects":[objects mentioned in the caption], "relationships":[[object index from object list, relationship extract from the caption, object index]]}"""
    prompt_caption = """You are a system designed for identifying objects and their relationships, known as a scene graph. When I describe a photo, artwork, or image, your role is to point out the objects and their relationships from that description. Additionally, include a background summary to create the scene graph. Your analysis should solely rely on the provided description. Present your findings in this structure: Scene Graph:"{} Background prompt.txt: . See the example below to understand the required format:\n{}""".format(
        scene_graph_format, default_caption)
    bounding_box_format = """Objects:[[object name, [top-left x coordinate, top-left y coordinate, box width, box height]]]"""
    prompt_scene_graph = """You are a smart bounding box creator. I will present you with a scene graph, a comprehensive outline containing objects and their relationships. Based on this, your responsibility is to predict bounding boxes location for the objects identified in the scene graph, factoring in their relationships. Bear in mind that the images are sized at 512x512 pixels; hence, it's imperative to ensure the bounding boxes don't overlap or extend outside the image's boundaries. Each bounding box should conform to the following format:{}. It's vital to produce a bounding box for each object mentioned in the scene graph, and these should mirror the provided relationships. Additionally, consider the object reasonable size  when determining the appropriate size for each bounding box. You can make informed assumptions if you are in doubt, but always keep the object relationships as a reference. For clarity on the format, refer to the example provided below.\n{}""".format(
        bounding_box_format, default_scene_graph)
    return prompt_caption, prompt_scene_graph


def append_message(role, content):
    messages.append({"role": role, "content": content})
    # if messages > 2, then delete the first one

    if len(messages) > 1:
        messages.pop(0)


def log_used_prompt(response, interface_name):
    example_num = 1
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    total_tokens = response.usage.total_tokens

    # formulate the above information into a string
    log_string = "----------------------------------------\n"
    log_string += "[Interface]: " + interface_name + "\n"
    log_string += "[Prompt tokens]: " + str(prompt_tokens) + "\n"
    log_string += "[Number of examples]: " + str(example_num) + "\n"
    log_string += "[Completion tokens]: " + str(completion_tokens) + "\n"
    log_string += "[Total tokens]: " + str(total_tokens) + "\n"
    # add a border
    log_string += "----------------------------------------\n"
    print(log_string)


def request_from_gpt(request, stage):
    """Use the davinci engine to request a completion from the API."""
    # prompt.txt = request
    # model = "text-davinci-003"
    #
    # completions = openai.Completion.create(
    #     engine=model,
    #     prompt.txt=prompt.txt,
    #     max_tokens=1024,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    # )
    #
    # message = completions.choices[0].text
    # return message

    """Use the gpt-3.5-turbo to request a completion from the API."""
    print("request:", request)
    append_message("user", request)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        # temperature=0.6,
        # max_tokens=2000,  # Adjust the value as per your requirement
        # n = 1, # Number of completions to generate
        # stop = '\n' # Stop generating completions after the first line break
    )
    log_used_prompt(response, stage)
    append_message("assistant", response.choices[0].message.content)
    return response.choices[0].message.content


def draw_scene_graph(objs, triples, output_folder, image_id, output_filename="graph.png", orientation='V',
                     edge_width=6, arrow_size=1.5, binary_edge_weight=1.2):
    """
    Use GraphViz to draw a scene graph.

    Using this requires that GraphViz is installed. On Ubuntu 16.04 this is easy:
    sudo apt-get install graphviz
    """
    if orientation not in ['V', 'H']:
        raise ValueError('Invalid orientation "%s"' % orientation)
    rankdir = {'H': 'LR', 'V': 'TD'}[orientation]

    # General setup, and style for object nodes
    lines = [
        'digraph{',
        'graph [size="5,3",ratio="compress",dpi="300",bgcolor="white"]',
        'rankdir=%s' % rankdir,
        'nodesep="0.5"',
        'ranksep="0.5"',
        'node [shape="box",style="rounded,filled",fontsize="48",color="none"]',
        'node [fillcolor="lightpink1"]',
    ]
    # Output nodes for objects
    for i, obj in enumerate(objs):
        lines.append('%d [label="%s"]' % (i, obj))

    # Output relationships
    next_node_id = len(objs)
    lines.append('node [fillcolor="lightblue1"]')
    for s, p, o in triples:
        lines += [
            '%d [label="%s"]' % (next_node_id, p),
            '%d->%d [penwidth=%f,arrowsize=%f,weight=%f]' % (
                s, next_node_id, edge_width, arrow_size, binary_edge_weight),
            '%d->%d [penwidth=%f,arrowsize=%f,weight=%f]' % (
                next_node_id, o, edge_width, arrow_size, binary_edge_weight)
        ]
        next_node_id += 1
    lines.append('}')

    # Write the graphviz spec to a temporary text file
    ff, dot_filename = tempfile.mkstemp()
    with open(dot_filename, 'w') as f:
        for line in lines:
            f.write('%s\n' % line)
    os.close(ff)

    # Invoke graphviz; this will save the resulting image to disk,
    # so we read it, delete it, then return it.
    output_format = os.path.splitext(output_filename)[1][1:]
    os.system('dot -T%s %s > %s' % (output_format, dot_filename, output_filename))
    os.remove(dot_filename)
    img = cv2.imread(output_filename)

    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Generate the output filename with the folder path, timestamp, and original filename
    output_file = f"{output_folder}/{timestamp}_image_{image_id}_graph.png"

    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the image with the new filename
    cv2.imwrite(output_file, img)
    os.remove(output_filename)
    return img


def draw_boxes(anns, output_folder, image_id):
    ax = plt.gca()
    # ax.set_autoscale_on(False)
    polygons = []
    color = []
    for ann in anns:
        c = (np.random.random((1, 3)) * 0.6 + 0.4)
        [bbox_x, bbox_y, bbox_w, bbox_h] = ann['bbox']
        poly = [[bbox_x, bbox_y], [bbox_x, bbox_y + bbox_h],
                [bbox_x + bbox_w, bbox_y + bbox_h], [bbox_x + bbox_w, bbox_y]]
        np_poly = np.array(poly).reshape((4, 2))
        polygons.append(Polygon(np_poly))
        color.append(c)

        # print(ann)
        name = ann['name'] if 'name' in ann else str(ann['category_id'])
        ax.text(bbox_x, bbox_y, name, style='italic',
                bbox={'facecolor': 'white', 'alpha': 0.7, 'pad': 5})

    p = PatchCollection(polygons, facecolor='none',
                        edgecolors=color, linewidths=2)
    ax.add_collection(p)

    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Generate the output filename with the folder path, timestamp, and object name
    output_filename = f"{output_folder}/{timestamp}_image_{image_id}_objects.png"

    # Save the image with the new filename
    plt.savefig(output_filename)

    # plt.show()


def show_boxes(gen_boxes, size, output_folder, image_id, bg_prompt=None):
    anns = [{'name': gen_box[0], 'bbox': gen_box[1]}
            for gen_box in gen_boxes]

    # White background (to allow line to show on the edge)
    I = np.ones((size[0] + 4, size[1] + 4, 3), dtype=np.uint8) * 255

    plt.imshow(I)
    draw_boxes(anns, output_folder, image_id)


def visualize_objects_with_boxes(objects, output_folder, image_id):
    box_scale = (512, 512)
    size = box_scale

    # Set a white background with the specified size
    background = np.ones((size[1], size[0], 3))
    plt.imshow(background)

    # Save and Visualize the Bounding box
    plt.figure(figsize=(8, 8))
    show_boxes(objects, box_scale, output_folder, image_id)


# sort the objects with its location
def reorder_objects(scene_graph, objects):
    final_order = []

    # Adjust order based on relationships
    for rel in scene_graph["relationships"]:
        if rel[0] >= len(scene_graph["objects"]) or rel[2] >= len(scene_graph["objects"]):
            continue
        A = scene_graph["objects"][rel[0]].split('_')[0]  # Get base name
        B = scene_graph["objects"][rel[2]].split('_')[0]  # Get base name

        if rel[1] == "in front of":
            if A not in final_order and B not in final_order:
                final_order.append(A)
                final_order.append(B)
            elif A in final_order and B not in final_order:
                final_order.insert(final_order.index(A) + 1, B)
            elif B in final_order and A not in final_order:
                final_order.insert(final_order.index(B), A)
            # print(final_order)
        elif rel[1] == "behind":
            if A not in final_order and B not in final_order:
                final_order.append(B)
                final_order.append(A)
            elif A in final_order and B not in final_order:
                final_order.insert(final_order.index(A), B)
            elif B in final_order and A not in final_order:
                final_order.insert(final_order.index(B) + 1, A)
            # print(final_order)

    # Add objects not in relationships to the end
    for obj in objects:
        obj_name = obj[0].split('_')[0]
        if obj_name not in final_order:
            final_order.append(obj_name)

    # Convert base names back to original objects
    object_mapping = {obj[0].split('_')[0]: obj for obj in objects}
    return [object_mapping[obj] for obj in final_order]


def add_objects_with_timestamp(new_data, file_path):
    """
    Add new objects with a timestamp to the existing JSON file.

    Parameters:
    - new_objects (list): List of tuples containing objects to be added.
    - file_path (str): Path to the JSON file.
    """
    try:
        # Try to load the current data from the JSON file
        with open(file_path, 'r') as file:
            current_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, initialize with an empty list
        current_data = []

        # Add a timestamp to each new object and append it to the current data
    timestamped_objects = [new_data, datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    current_data.extend(timestamped_objects)

    # Write the updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(current_data, file)


def main(caption):
    # Extract the default_caption default_scene_graph from the train.json
    train_data = "Backend/data/train.json"
    default_caption, default_scene_graph = get_prompt_caption(train_data)
    # print("Default Caption:", default_caption)
    # print("Default Scene Graph:", default_scene_graph)

    # User input the caption
    user_input = caption
    user_caption = default_caption + "\n" + "\nCaption:" + user_input + "\n" + "Scene Graph:"
    print(user_caption)

    # Return the Scene Graph and Background prompt.txt
    caption = request_from_gpt(user_caption, "Stage1: Get the Scene Graph")

    # Split the string into scene graph and background prompt.txt
    scene_graph_str, background_prompt = caption.split('Background prompt.txt:', 1)
    background_prompts[0] = background_prompt

    # Convert the scene graph string to a dictionary
    scene_graph = literal_eval(scene_graph_str.strip())
    scene_graph, background_prompt.strip()
    print("Scene Graph:", scene_graph)
    print("Background Promote:", background_prompt)

    # Predict the layout of the object
    scene_graph_prompt = default_scene_graph + "\n" + "Scene Graph: " + str(scene_graph) + "\n" + "Objects: "
    layout = request_from_gpt(scene_graph_prompt, "Stage2: Get the Layout")
    print("Predicted Layout:", layout)

    # Save and Visualize the Bounding box
    objects_layout = literal_eval(layout)
    reordered_objects = reorder_objects(scene_graph, objects_layout)
    print("Reordered objects by its location:", reordered_objects)

    return scene_graph, background_prompt, reordered_objects


def generate_image(background_prompt, reordered_objects, generate_index = 0
                   ):
    """
    overall_prompt_override = ""
    seed = 0
    num_inference_steps = 1
    dpm_scheduler = False
    use_autocast = False
    fg_seed_start = 20
    fg_blending_ratio = 0.1
    frozen_step_ratio = 0.5
    attn_guidance_step_ratio = 0.6
    gligen_scheduled_sampling_beta = 0.4
    attn_guidance_scale = 20
    use_ref_ca = False
    so_negative_prompt = DEFAULT_SO_NEGATIVE_PROMPT
    overall_negative_prompt = DEFAULT_OVERALL_NEGATIVE_PROMPT
    show_so_imgs = False
    scale_boxes = False

    print("origin bb:", reordered_objects, "length:", len(reordered_objects))
    spec = {
        # prompt is unused
        'prompt': '',
        'gen_boxes': reordered_objects,
        'bg_prompt': background_prompt,
        'extra_neg_prompt': ''
    }

    if dpm_scheduler:
        scheduler_key = "dpm_scheduler"
    else:
        scheduler_key = "scheduler"

    overall_max_index_step = int(attn_guidance_step_ratio * num_inference_steps)

    image_np, so_img_list = run_ours(
        spec, bg_seed=seed, overall_prompt_override=overall_prompt_override, fg_seed_start=fg_seed_start,
        fg_blending_ratio=fg_blending_ratio, frozen_step_ratio=frozen_step_ratio, use_autocast=use_autocast,
        so_gligen_scheduled_sampling_beta=gligen_scheduled_sampling_beta,
        overall_gligen_scheduled_sampling_beta=gligen_scheduled_sampling_beta,
        num_inference_steps=num_inference_steps, scheduler_key=scheduler_key,
        use_ref_ca=use_ref_ca, so_negative_prompt=so_negative_prompt,
        overall_negative_prompt=overall_negative_prompt,
        loss_scale=attn_guidance_scale, max_index_step=0, overall_loss_scale=attn_guidance_scale,
        overall_max_index_step=overall_max_index_step, generate_index = generate_index
    )

    images = [image_np]
    if show_so_imgs:
        images.extend([np.asarray(so_img) for so_img in so_img_list])
    """
    return np.zeros((512, 512, 3))

def create_new_task_id():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"task_{timestamp}"
def generate_image_task(background_prompt, reordered_objects, task_id):

    images = generate_image(background_prompt, reordered_objects)



def start_image_generation(background_prompt, reordered_objects):
    task_id = create_new_task_id()
    thread = Thread(target=generate_image_task, args=(background_prompt, reordered_objects, task_id))
    thread.start()
    return task_id

@app.route('/api/test/hello/', methods=["GET", "POST"])
def hello_resp():
    if request.method == "POST":
        print("run")
        data = request.get_data().decode("utf-8")
        caption = literal_eval(data)
        print(caption["caption"])
        scene_graph, background_prompt, reordered_objects = main(caption["caption"])

        # Load the existing output JSON
        output_file_path = 'Backend/output/output.json'
        output_photo_path = 'Backend/output/photos'

        # Check if the file exists and has content
        try:
            with open(output_file_path, 'r') as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = []  # If not found or empty, create an empty list

        # Extract the current image numbers from the data
        image_numbers = [int(entry["Image_id"].split('.')[0]) for entry in data if "Image_id" in entry]

        # Determine the next image number
        next_image_number = max(image_numbers) + 1 if image_numbers else 1

        # Check if the caption already exists in the data
        existing_entry = next((entry for entry in data if entry["Caption"] == caption), None)

        task_id = start_image_generation(background_prompt, reordered_objects)

        #images = generate_image(background_prompt, reordered_objects)

        # For generate the image
        # # Generate a timestamp
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        #
        # # Generate the output filename with the folder path, timestamp, and object name
        # output_photo = f"{output_photo_path}/{timestamp}_image.png"

        # overall_prompt_override = ""
        # seed = 0
        # num_inference_steps = 250
        # dpm_scheduler = True
        # use_autocast = False
        # fg_seed_start = 20
        # fg_blending_ratio = 0.1
        # frozen_step_ratio = 0.5
        # attn_guidance_step_ratio = 0.6
        # gligen_scheduled_sampling_beta = 0.4
        # attn_guidance_scale = 20
        # use_ref_ca = True
        # so_negative_prompt = DEFAULT_SO_NEGATIVE_PROMPT
        # overall_negative_prompt = DEFAULT_OVERALL_NEGATIVE_PROMPT
        # show_so_imgs = False
        # scale_boxes = False
        #
        # spec = {
        #     # prompt is unused
        #     'prompt': '',
        #     'gen_boxes': reordered_objects,
        #     'bg_prompt': background_prompt,
        #     'extra_neg_prompt': ''
        # }
        #
        # if dpm_scheduler:
        #     scheduler_key = "dpm_scheduler"
        # else:
        #     scheduler_key = "scheduler"
        #
        # overall_max_index_step = int(attn_guidance_step_ratio * num_inference_steps)
        #
        # image_np, so_img_list = run_ours(
        #     spec, bg_seed=seed, overall_prompt_override=overall_prompt_override, fg_seed_start=fg_seed_start,
        #     fg_blending_ratio=fg_blending_ratio, frozen_step_ratio=frozen_step_ratio, use_autocast=use_autocast,
        #     so_gligen_scheduled_sampling_beta=gligen_scheduled_sampling_beta,
        #     overall_gligen_scheduled_sampling_beta=gligen_scheduled_sampling_beta,
        #     num_inference_steps=num_inference_steps, scheduler_key=scheduler_key,
        #     use_ref_ca=use_ref_ca, so_negative_prompt=so_negative_prompt,
        #     overall_negative_prompt=overall_negative_prompt,
        #     loss_scale=attn_guidance_scale, max_index_step=0, overall_loss_scale=attn_guidance_scale,
        #     overall_max_index_step=overall_max_index_step,
        # )
        #
        # images = [image_np]
        # if show_so_imgs:
        #     images.extend([np.asarray(so_img) for so_img in so_img_list])

        if existing_entry:
            # Update the existing entry
            existing_entry["Scene Graph"] = scene_graph
            existing_entry["Objects"] = reordered_objects
            existing_entry["Background prompt"] = background_prompt
        else:
            # Append a new entry
            new_entry = {
                "Image_id": f"{next_image_number}.jpg",
                "Caption": caption,
                "Scene Graph": scene_graph,
                "Objects": reordered_objects,
                "Background prompt": background_prompt
            }
            data.append(new_entry)

            # Save the updated data back to the JSON file
        with open(output_file_path, 'w') as file:
            json.dump(data, file, indent=4)
            print("Saved to", output_file_path)

        return {'sc': scene_graph, "ro": reordered_objects, "bp": background_prompt}


@app.route('/api/test/getLayout/', methods=['GET', 'POST'])
def getLayout():
    timer[0] = timer[0] + 1
    layoutStr = request.form["layoutStr"]
    print("LayoutStr")
    print(layoutStr)
    layoutObjs=layoutStr.split(';')
    layoutList=[]
    for i in range(len(layoutObjs)-1):
        layouts=layoutObjs[i].split(',')
        layoutList.append(([layouts[0], [int(float(layouts[1])), int(float(layouts[2])), int(float(layouts[3])), int(float(layouts[4]))]]))
    #layout=json.dumps(layoutList)
    #layout=layoutList.replace('\"', '\'')
    #print(layout)
    #print(type(layout))
    print(len(layoutList))
    generate_image(background_prompts[0],layoutList, generate_index = timer[0])
    return jsonify({"error": 1001, "msg": "上传失败"})









# @app.route('/getPoint/',methods=['GET','POST'])
# def getPoint():
#     ids=list(json.loads(request.args.get('key')))
#     print(ids[0])
#     xs=list(json.loads(request.args.get('x')))
#     ys=list(json.loads(request.args.get('y')))
#     print(xs[0])
#     print(ys[0])
#     return jsonify({"error": 1001, "msg": "上传失败"})
# @app.route('/getValue/',methods=['GET'])
# def getValue():
#     return jsonify(va)    

# @app.route('/api/test/getPrompt/',methods=['GET','POST'])
# def getPrompt():
#     query = request.form["text"]
#     query_features=text_model.encode([query], convert_to_tensor=False)
#     prompt_KNNs=prompt_ball_search_C(query_features[0], 500)
#     temps=[]
#     c=0
#     idx=0
#     while c<50:
#         if prompts[prompt_KNNs[idx]] not in temps:
#             temps.append(prompts[prompt_KNNs[idx]])
#             c=c+1
#         idx=idx+1
#     for i in range(50):
#         searchPrompts[i]=temps[i]
#     return jsonify({"error": 1001, "msg": "上传失败"})
#
# @app.route('/api/test/fetchPrompt/',methods=['GET','POST'])
# def fetchPrompt():
#     path_dic={}
#     for i in range(50):
#         # with open(va[i], 'rb') as img_f:
#         #     img_stream = img_f.read()
#         #     img_stream = base64.b64encode(img_stream)
#         path_dic[str(i)] = searchPrompts[i]
#     # print(path_dic)
#     return jsonify(path_dic)#jsonify({"0": va[0], "1": va[1],"2":va[2],"3": va[3],"4":va[4],"5": va[5], "6": va[6], "7": va[7], "8": va[8], "9": va[9]})
#
# @app.route('/api/test/postGenerate/',methods=['GET','POST'])
# def postGenerate():
#     query = request.form["text"]
#     t=time.localtime()
#     t_suffix=str(t.tm_year)+"_"+str(t.tm_mon)+"_"+str(t.tm_mday)+"_"+str(t.tm_hour)+"_"+str(t.tm_min)+"_"+str(t.tm_sec)
#     path_dic={}
#     path_list=[]
#     imgs=[]
#     generated_paths[0]=['' for i in range(sample_len)]
#     for i in range(sample_len):
#         seed=(int)(1000000*random.random())
#         all_seeds[i]=seed
#         generator = torch.Generator("cuda").manual_seed(seed)
#         image = pipe(query, generator=generator).images[0]
#         im_path=str(i)+"_"+t_suffix+".png"
#         image.save("D:/Test_Disen/Frontend/src/assets/testGen/"+im_path)
#         path_dic[str(i)]=im_path
#         path_list.append(im_path)
#         # im=Image.open(seg_path)
#         # im = Image.open(byte_stream)
#         width, height = image.size
#         imgs.append(preprocess(image))
#         generated_paths[0][i]=im_path
#     image_input = torch.tensor(np.stack(imgs)).cuda()
#     with torch.no_grad():
#         image_features = clip_model.encode_image(image_input).float()
#     image_features /= image_features.norm(dim=-1, keepdim=True)
#     im_features=image_features.cpu().numpy()
#     print(im_features.shape)
#     all_embeds[0]=im_features
#     tsne = manifold.TSNE(n_components=2, init='pca', random_state=501, metric='cosine', perplexity=5)
#     pre1_t=tsne.fit_transform(im_features)
#     x_min, x_max = pre1_t.min(0), pre1_t.max(0)
#     pre1_norm = (pre1_t - x_min) / (x_max - x_min)
#     print(pre1_norm.shape)
#     print(pre1_norm)
#     try:
#         os.remove('D:/Test_Disen/Frontend/src/assets/testSample1.csv')
#     except:
#         e=1
#     with open('D:/Test_Disen/Frontend/src/assets/testSample1.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(["prompt","x","y","path", "id"])
#         for i in range(sample_len):
#             writer.writerow([query, pre1_norm[i][0], pre1_norm[i][1], path_list[i], 0])
#     return jsonify(path_dic)
#
# @app.route('/api/test/postAxis/',methods=['GET','POST'])
# def postAxis():
#     num = int(request.form["num"])
#     concepts=[]
#     concepts2=[]
#     types=[]
#     for i in range(num):
#         concepts.append(request.form["concept"+str(i)])
#         types.append(request.form["type"+str(i)])
#         concepts2.append('')
#     for i in range(num):
#         if types[i]=="double":
#             concepts2[i]=request.form["concept"+str(i)+"double"]
#     current_concepts[0]=concepts
#     imgs=[]
#     for i in range(len(generated_paths[0])):
#         image=Image.open("D:/Test_Disen/Frontend/src/assets/testGen/"+generated_paths[0][i])
#         imgs.append(preprocess(image))
#     image_input = torch.tensor(np.stack(imgs)).cuda()
#     with torch.no_grad():
#         image_features = clip_model.encode_image(image_input).float()
#     image_features /= image_features.norm(dim=-1, keepdim=True)
#     im_features=image_features.cpu().numpy()
#
#     # for i in range(sample_len):
#     features=[]
#     for j in range(num):
#         text_tokens = clip.tokenize(concepts[j]).cuda()
#         with torch.no_grad():
#             text_features = clip_model.encode_text(text_tokens).float()
#         text_features /= text_features.norm(dim=-1, keepdim=True)
#         text_features=text_features.cpu().numpy()
#         if types[j]=="single":
#             features.append(text_features @ im_features.T)
#         else:
#             text_tokens2 = clip.tokenize(concepts2[j]).cuda()
#             with torch.no_grad():
#                 text_features2 = clip_model.encode_text(text_tokens2).float()
#             text_features2 /= text_features2.norm(dim=-1, keepdim=True)
#             text_features2=text_features2.cpu().numpy()
#             sim1=text_features @ im_features.T
#             sim2=text_features2 @ im_features.T
#             features.append(0.5+(sim1-sim2)/(sim1+sim2))
#
#
#     print(features[0].shape)
#
#     for n in range(num):
#         try:
#             os.remove('D:/Test_Disen/Frontend/src/assets/testSample_Axis'+str(n)+'.csv')
#         except:
#             e=1
#         with open('D:/Test_Disen/Frontend/src/assets/testSample_Axis'+str(n)+'.csv', 'w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(["correlation", "id"])
#
#             for i in range(len(generated_paths[0])):
#                 idx=0
#                 if i>=sample_len:
#                     idx=1
#                 writer.writerow([features[n][0][i], idx])
#
#     return jsonify({"error": 1001, "msg": "上传失败"})
#
# @app.route('/api/test/addGenerate/',methods=['GET','POST'])
# def addGenerate():
#     query = request.form["text"]
#     num_id= request.form["num_id"]
#     t=time.localtime()
#     t_suffix=str(t.tm_year)+"_"+str(t.tm_mon)+"_"+str(t.tm_mday)+"_"+str(t.tm_hour)+"_"+str(t.tm_min)+"_"+str(t.tm_sec)
#     path_dic={}
#     path_list=[]
#     imgs=[]
#     generated_paths[0]=generated_paths[0][:sample_len]
#     for i in range(sample_len):
#         image=Image.open("D:/Test_Disen/Frontend/src/assets/testGen/"+generated_paths[0][i])
#         imgs.append(preprocess(image))
#     for i in range(sample_len):
#         seed=all_seeds[i]
#         generator = torch.Generator("cuda").manual_seed(seed)
#         image = pipe(query, generator=generator).images[0]
#         im_path=str(i)+"_"+t_suffix+".png"
#         image.save("D:/Test_Disen/Frontend/src/assets/testGen/"+im_path)
#         path_dic[str(i)]=im_path
#         path_list.append(im_path)
#         # im=Image.open(seg_path)
#         # im = Image.open(byte_stream)
#         width, height = image.size
#         imgs.append(preprocess(image))
#         generated_paths[0].append(im_path)
#         # generated_paths
#     image_input = torch.tensor(np.stack(imgs)).cuda()
#     with torch.no_grad():
#         image_features = clip_model.encode_image(image_input).float()
#     image_features /= image_features.norm(dim=-1, keepdim=True)
#     im_features=image_features.cpu().numpy()
#     all_embeds[1]=im_features
#     print(im_features.shape)
#     tsne = manifold.TSNE(n_components=2, init='pca', random_state=501, metric='cosine', perplexity=5)
#     pre1_t=tsne.fit_transform(im_features)
#     x_min, x_max = pre1_t.min(0), pre1_t.max(0)
#     pre1_norm = (pre1_t - x_min) / (x_max - x_min)
#     print(pre1_norm.shape)
#     print(pre1_norm)
#     try:
#         os.remove('D:/Test_Disen/Frontend/src/assets/testSample1.csv')
#     except:
#         e=1
#     with open('D:/Test_Disen/Frontend/src/assets/testSample1.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(["prompt","x","y","path","id"])
#         for i in range(len(generated_paths[0])):
#             idx=0
#             if i>=sample_len:
#                 idx=1
#             writer.writerow([query, pre1_norm[i][0], pre1_norm[i][1], generated_paths[0][i], idx])
#
#     return jsonify(path_dic)
#
# @app.route('/api/test/postContext/',methods=['GET','POST'])
# def postContext():
#     num = int(request.form["num"])
#     # word_cluster_size=3
#     word_cluster_size=2
#     concepts=[]
#     concepts2=[]
#     types=[]
#     for i in range(num):
#         concepts.append(request.form["concept"+str(i)])
#         types.append(request.form["type"+str(i)])
#         concepts2.append('')
#     for i in range(num):
#         if types[i]=="double":
#             concepts2[i]=request.form["concept"+str(i)+"double"]
#     current_concepts[0]=concepts
#     imgs=[]
#     all_im_paths=[]
#     all_concept_ems=[]
#     for i in range(len(generated_paths[0])):
#         image=Image.open("D:/Test_Disen/Frontend/src/assets/testGen/"+generated_paths[0][i])
#         all_im_paths.append(generated_paths[0][i])
#         imgs.append(preprocess(image))
#     image_input = torch.tensor(np.stack(imgs)).cuda()
#     with torch.no_grad():
#         image_features = clip_model.encode_image(image_input).float()
#     image_features /= image_features.norm(dim=-1, keepdim=True)
#     im_features=image_features.cpu().numpy()
#     all_concepts=[]
#     for i in range(num):
#         all_concepts.append(concepts[i])
#         if concepts2[i]!='':
#             all_concepts.append(concepts2[i])
#     text_ems=[]
#     for j in range(len(all_concepts)):
#         text_tokens = clip.tokenize(all_concepts[j]).cuda()
#         with torch.no_grad():
#             text_features = clip_model.encode_text(text_tokens).float()
#         text_features /= text_features.norm(dim=-1, keepdim=True)
#         text_features=text_features.cpu().numpy()
#         text_ems.append(text_features)
#         knns=knn_search_C(text_features[0],im_features,word_cluster_size)
#         ems0=im_features[knns[0]]
#         for w in range(1, word_cluster_size):
#             ems0=ems0+im_features[knns[w]]
#         concept_em=ems0/word_cluster_size
#         all_concept_ems.append(concept_em)
#     print("concept_em")
#     print(all_concept_ems[0].shape)
#     print("im_features")
#     print(im_features.shape)
#     ems_list=[im_features]
#     for i in range(len(all_concept_ems)):
#         ems_list.append(all_concept_ems[i].reshape((1,-1)))
#     all_ems=np.concatenate(ems_list)
#
#     current_all_ems[0]=all_ems
#
#     tsne = manifold.TSNE(n_components=2, init='pca', random_state=501, metric='cosine', perplexity=5)
#     pre1_t=tsne.fit_transform(all_ems)
#     x_min, x_max = pre1_t.min(0), pre1_t.max(0)
#     pre1_norm = (pre1_t - x_min) / (x_max - x_min)
#     print(pre1_norm.shape)
#
#     try:
#         os.remove('D:/Test_Disen/Frontend/src/assets/testSampleCon.csv')
#     except:
#         e=1
#     print("check-inner-product")
#     print((text_ems[0]@ im_features[0].T).shape)
#     with open('D:/Test_Disen/Frontend/src/assets/testSampleCon.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         headers=["prompt","x","y","path","id"]
#         for i in range(len(all_concepts)):
#             headers.append("concept"+str(i+1))
#             # headers.append(all_concepts[i])
#         # writer.writerow(["prompt","x","y","path","id"])
#         writer.writerow(headers)
#
#         for i in range(len(generated_paths[0])):
#             idx=0
#             entry=['query', pre1_norm[i][0], pre1_norm[i][1], generated_paths[0][i], idx]
#             for j in range(len(all_concepts)):
#                 sc=np.sum(text_ems[j]@ im_features[i].T)
#                 entry.append(sc)
#             if i>=sample_len:
#                 idx=1
#             # writer.writerow(['query', pre1_norm[i][0], pre1_norm[i][1], generated_paths[0][i], idx])
#             writer.writerow(entry)
#         for i in range(len(generated_paths[0]), len(generated_paths[0])+len(all_concept_ems)):
#             entry=[all_concepts[i-len(generated_paths[0])], pre1_norm[i][0], pre1_norm[i][1], '', 2]
#             for j in range(len(all_concepts)):
#                 sc=np.sum(text_ems[j]@ text_ems[i-len(generated_paths[0])].T)
#                 entry.append(sc)
#             writer.writerow(entry)
#             # writer.writerow([all_concept_ems[i-len(generated_paths[0])], pre1_norm[i][0], pre1_norm[i][1], '', 2])
#
#     return jsonify({"error": 1001, "msg": "上传失败"})
#
# @app.route('/api/test/postPath/',methods=['GET','POST'])
# def postPath():
#     neighbor_size=3
#     num = int(request.form["num"])
#     concepts=[]
#     concepts2=[]
#     types=[]
#     for i in range(num):
#         concepts.append(request.form["concept"+str(i)])
#         types.append(request.form["type"+str(i)])
#         concepts2.append('')
#     for i in range(num):
#         if types[i]=="double":
#             concepts2[i]=request.form["concept"+str(i)+"double"]
#     imgs=[]
#     for i in range(len(generated_paths[0])):
#         image=Image.open("D:/Test_Disen/Frontend/src/assets/testGen/"+generated_paths[0][i])
#         imgs.append(preprocess(image))
#     image_input = torch.tensor(np.stack(imgs)).cuda()
#     with torch.no_grad():
#         image_features = clip_model.encode_image(image_input).float()
#     image_features /= image_features.norm(dim=-1, keepdim=True)
#     im_features=image_features.cpu().numpy()
#     features=[]
#     for j in range(num):
#         text_tokens = clip.tokenize(concepts[j]).cuda()
#         with torch.no_grad():
#             text_features = clip_model.encode_text(text_tokens).float()
#         text_features /= text_features.norm(dim=-1, keepdim=True)
#         text_features=text_features.cpu().numpy()
#         if types[j]=="single":
#             features.append(text_features @ im_features.T)
#         else:
#             text_tokens2 = clip.tokenize(concepts2[j]).cuda()
#             with torch.no_grad():
#                 text_features2 = clip_model.encode_text(text_tokens2).float()
#             text_features2 /= text_features2.norm(dim=-1, keepdim=True)
#             text_features2=text_features2.cpu().numpy()
#             sim1=text_features @ im_features.T
#             sim2=text_features2 @ im_features.T
#             features.append(0.5+(sim1-sim2)/(sim1+sim2))
#     print("features")
#     print(features[0].shape)
#     print(len(features))
#     Cscores=[]
#     for i in range(len(generated_paths[0])):
#         Cscores.append(features[0][0][i])
#     max_id=np.argmax(Cscores)
#     min_id=np.argmin(Cscores)
#     print("max_id")
#     print(max_id)
#     print("min_id")
#     print(min_id)
#     path_list=[min_id]
#     current_id=min_id
#     current_score=Cscores[current_id]
#     while current_id!=max_id:
#         neighbor_size=3
#         next_id=current_id
#         while next_id==current_id:
#             knns=knn_search_C(im_features[current_id],im_features,neighbor_size)
#             for i in range(neighbor_size):
#                 if Cscores[knns[i]]>Cscores[next_id]:
#                     next_id=knns[i]
#             neighbor_size=neighbor_size+1
#         current_id=next_id
#         path_list.append(current_id)
#     if len(control_points[0])==0:
#         for i in range(len(path_list)):
#             control_points[0].append(im_features[path_list[i]])
#             control_ids[0].append(path_list[i])
#     else:
#         control_points[0]=[]
#         control_ids[0]=[]
#         for i in range(len(path_list)):
#             control_points[0].append(im_features[path_list[i]])
#             control_ids[0].append(path_list[i])
#     path_str=""
#     for i in range(len(path_list)):
#         path_str=path_str+str(path_list[i])+","
#     # if num==1:
#     #     if request.form["type0"]=="single":
#     #         for
#     return jsonify({"path_len": len(path_list), "path_str": path_str})
#
# @app.route('/api/test/postLAMP/',methods=['GET','POST'])
# def postLAMP():
#     xs=request.form["control_xs"]
#     ys=request.form["control_ys"]
#     xs_str=xs.split(",")
#     ys_str=ys.split(",")
#     for i in range(len(xs_str)):
#         if xs_str[i]!="":
#             projected_anchors[0].append(np.array([float(xs_str[i]),float(ys_str[i])]))
#
#     imgs=[]
#     # for i in range(len(generated_paths[0])):
#     #     image=Image.open("D:/Test_Disen/Frontend/src/assets/testGen/"+generated_paths[0][i])
#     #     imgs.append(preprocess(image))
#     # image_input = torch.tensor(np.stack(imgs)).cuda()
#     # with torch.no_grad():
#     #     image_features = clip_model.encode_image(image_input).float()
#     # image_features /= image_features.norm(dim=-1, keepdim=True)
#     # im_features=image_features.cpu().numpy()
#     im_features=current_all_ems[0]
#     c=0
#     new_projections=[]
#     lines=[]
#     headers=[]
#     lc=0
#     with open("Frontend/src/assets/testSampleCon.csv") as f:
#         csvreader = csv.reader(f)
#         for line in csvreader:
#             if lc>0:
#                 lines.append(line)
#             else:
#                 headers=line
#             lc=lc+1
#     for i in range(len(lines)):
#         x_matrix=[]
#         y_matrix=[]
#         if i not in control_ids[0]:
#             alphas=[1/((np.linalg.norm(im_features[i]-im_features[idx]))**2) for idx in control_ids[0]]
#             alpha=np.sum(alphas)
#             x_cur=alphas[0]*im_features[control_ids[0][0]]
#             y_cur=alphas[0]*projected_anchors[0][0]
#             for k in range(1,len(control_ids[0])):
#                 x_cur=x_cur+alphas[k]*im_features[control_ids[0][k]]
#                 y_cur=y_cur+alphas[k]*projected_anchors[0][k]
#             x_cur=x_cur/alpha
#             y_cur=y_cur/alpha
#             for k in range(len(control_ids[0])):
#                 x_matrix.append(np.sqrt(alphas[k])*(im_features[control_ids[0][k]]-x_cur))
#                 y_matrix.append(np.sqrt(alphas[k])*(projected_anchors[0][k]-y_cur))
#
#             x_np=np.stack(x_matrix, axis=0)
#             y_np=np.stack(y_matrix, axis=0)
#             atb=x_np.T @ y_np
#             U, S, Vh = np.linalg.svd(atb, full_matrices=False)
#             M = U @ Vh
#             new_pro=(im_features[i]-x_cur) @ M + y_cur
#             new_projections.append(new_pro)
#             if c==0:
#                 print("x_np")
#                 print(x_np.shape)
#                 print("y_np")
#                 print(y_np.shape)
#                 print("atb")
#                 print(atb.shape)
#                 print("M")
#                 print(M.shape)
#                 print("new_pro")
#                 print(new_pro.shape)
#                 print(new_pro)
#                 c=1
#
#         else:
#             idx=control_ids[0].index(i)
#             print(idx)
#             new_projections.append(projected_anchors[0][idx])
#             print(projected_anchors[0][idx])
#
#
#
#
#     try:
#         os.remove('Frontend/src/assets/testSampleCon.csv')
#     except:
#         e=1
#
#     print("lines")
#     print(len(lines))
#     print("new_pros")
#     print(len(new_projections))
#
#     with open('Frontend/src/assets/testSampleCon.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         # writer.writerow(["prompt","x","y","path","id"])
#         writer.writerow(headers)
#         for i in range(len(lines)):
#             entry=[lines[i][0], new_projections[i][0], new_projections[i][1], lines[i][3], lines[i][4]]
#             ori_len=len(entry)
#             for j in range(ori_len,len(lines[i])):
#                 entry.append(lines[i][j])
#             writer.writerow(entry)
#             # writer.writerow([lines[i][0], new_projections[i][0], new_projections[i][1], lines[i][3], lines[i][4]])
#
#     projected_anchors[0]=[]
#
#
#
#     return jsonify({"error": 1001, "msg": "上传失败"})
#
# @app.route('/api/test/postBLIP/',methods=['GET','POST'])
# def postBLIP():
#     caps=[]
#     for i in range(len(generated_paths[0])):
#         image = Image.open("Frontend/src/assets/testGen"+generated_paths[0][i])
#         inputs = blip_processor(images=image, return_tensors="pt").to(device, torch.float16)
#         generated_ids = blip_model.generate(**inputs)
#         generated_text = blip_processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
#         caps.append(generated_text)
#     vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
#     X = vectorizer.fit_transform(caps)
#     # features = (vectorizer.get_feature_names())
#     keywords=vectorizer.get_feature_names_out()
#     # visual_concept_cans[0]=keywords
#     sums = X.sum(axis = 0)
#     data1 = []
#     for col, term in enumerate(keywords):
#         data1.append( (term, sums[0,col] ))
#     ranking = pd.DataFrame(data1, columns = ['term','rank'])
#     words = (ranking.sort_values('rank', ascending = False))
#     ranked_keywords=[]
#     for i in range(len(keywords)):
#         ranked_keywords.append(words.iloc[i]["term"])
#     visual_concept_cans[0]=ranked_keywords
#     try:
#         os.remove('Frontend/src/assets/testBlipVis.csv')
#     except:
#         e=1
#     with open('Frontend/src/assets/testBlipVis.csv', 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(["term"])
#         for i in range(len(ranked_keywords)):
#             writer.writerow([ranked_keywords[i]])
#
#     return jsonify({"error": 1001, "msg": "上传失败"})
if __name__ == "__main__":
    app.run(debug=True)
