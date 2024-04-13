import torch
from transformers import CLIPImageProcessor, CLIPModel, CLIPTokenizer
# from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import os
import pandas as pd
import cv2

# Load the CLIP model
from transformers import CLIPProcessor, CLIPModel
model = CLIPModel.from_pretrained("../clip-vit-base-patch16")
preprocess = CLIPImageProcessor.from_pretrained("../clip-vit-base-patch16")



# Define a function to load an image and preprocess it for CLIP
def load_and_preprocess_image(image_path):
    # Load the image from the specified path
    image = Image.open(image_path)
    # Apply the CLIP preprocessing to the image
    image = preprocess(image, return_tensors="pt")
    # Return the preprocessed image
    return image


def clip_img_score (img1_path,img2_path):
    # Load the two images and preprocess them for CLIP
    image_a = load_and_preprocess_image(img1_path)["pixel_values"]
    image_b = load_and_preprocess_image(img2_path)["pixel_values"]

    # Calculate the embeddings for the images using the CLIP model
    with torch.no_grad():
        embedding_a = model.get_image_features(image_a)
        embedding_b = model.get_image_features(image_b)

    # Calculate the cosine similarity between the embeddings
    similarity_score = torch.nn.functional.cosine_similarity(embedding_a, embedding_b)
    return similarity_score.item()


p_dic = [
    'weep_two_tree',
         'crepen_two_tree',
         'Banya_two_tree',
         'weep_jap',
         'crepen_alone',
         'Banya_lily',
         'dogwood_weep',
         'dogwood+lily',
         'Banya_jap',
         'weep_alone',
         'dogwood_alone',
         'dogwood_two_tree',
         'jap_two_tree',
         'jap_lily',
         'Banya_tulip',
         'Tulip',
         'weep_tulip',
         'dogwood_jap',
         'jap_tulip',
         'Banya_alone',
         'lily',
         # 'weep+banya',
         'dogwood_tulip',
         'jap_alone']


def extract_number_from_filename(filename):
    return int(filename.split('_')[-1].split('.')[0])


scores_dic = {}
path_root = "C:/Users/user/PycharmProjects/landscapeDesign/llm-grounded-diffusion/batch_result/9_8"
for p in p_dic:
    a_folder = os.path.join(path_root, p)
    b_folder = os.path.join(path_root, p + "__base")

    a_images = sorted(os.listdir(a_folder))
    b_images = sorted(os.listdir(b_folder))

    # 使用字典存储文件夹A和B中的图片
    a_dict = {extract_number_from_filename(img): img for img in a_images}
    b_dict = {extract_number_from_filename(img): img for img in b_images}

    common_numbers = set(a_dict.keys()) & set(b_dict.keys())

    scores_a = []
    scores_b = []
    a_init = ""
    b_init = ""
    for number in common_numbers:
        if a_init == "" and b_init == "":
            a_init = os.path.join(a_folder, a_dict[number])
            b_init = os.path.join(b_folder, b_dict[number])
            continue
        a_next = os.path.join(a_folder, a_dict[number])
        b_next = os.path.join(b_folder, b_dict[number])

        score_a = clip_img_score(a_init, a_next)
        score_b = clip_img_score(b_init, b_next)
        print(a_init, a_next, score_a)
        print(b_init, b_next, score_b)

        scores_a.append(score_a)
        scores_b.append(score_b)

        a_init = a_next
        b_init = b_next


        score_a_tmp = {p: scores_a}
        score_b_tmp = {p + "__base": scores_b}

        scores_dic[p] = scores_a
        scores_dic[p + "__base"] = scores_b

        data_a = pd.DataFrame(score_a_tmp)
        data_a.to_csv('sim/sim_{}.csv'.format(p), index=False)

        data_b = pd.DataFrame(score_b_tmp)
        data_b.to_csv('sim/sim_{}.csv'.format(p + "__base"), index=False)
data = pd.DataFrame(scores_dic)
data.to_csv('sim/sim_total.csv', index=False)
