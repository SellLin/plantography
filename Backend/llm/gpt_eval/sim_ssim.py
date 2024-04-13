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

import torch
import torch.nn.functional as F
from math import exp
import numpy as np

import pytorch_ssim
import torch
from torch.autograd import Variable
from torch import optim
import cv2
import numpy as np


# Module: pytorch_ssim.SSIM(window_size = 11, size_average = True)
ssim_loss = pytorch_ssim.SSIM()

# optimizer = optim.Adam([img2], lr=0.01)

# 创建一维高斯分布向量
def gaussian(window_size, sigma):
    gauss = torch.Tensor([exp(-(x - window_size // 2) ** 2) / float(2 * sigma ** 2) for x in range(window_size)])
    return gauss / gauss.sum()


# 创建高斯核
def create_window(window_size, channel=1):
    # unqueeze(1) 在第二维上增加一个维度
    _1D_window = gaussian(window_size, 1.5).unsqueeze(1)
    # t() 转置
    _2D_window = _1D_window.mm(_1D_window.t()).float().unsqueeze(0).unsqueeze(0)
    window = _2D_window.expand(channel, 1, window_size, window_size).contiguous()
    return window


# 计算ssim
# 采用归一化的高斯核来 代替计算像素的均值
def ssim(img1, img2, window, window_size, channel=1, size_average=True):
    mu1 = F.conv2d(img1, window, padding=window_size // 2, stride=1, groups=channel)
    mu2 = F.conv2d(img2, window, padding=window_size // 2, stride=1, groups=channel)

    mu1_sq = mu1.pow(2)
    mu2_sq = mu2.pow(2)
    mu1_mu2 = mu1 * mu2

    sigma1_sq = F.conv2d(img1 * img1, window, padding=window_size // 2, stride=1, groups=channel) - mu1_sq
    sigma2_sq = F.conv2d(img2 * img2, window, padding=window_size // 2, stride=1, groups=channel) - mu2_sq
    sigma_12 = F.conv2d(img1 * img2, window, padding=window_size // 2, stride=1, groups=channel) - mu1_mu2

    c1 = 0.01 ** 2
    c2 = 0.03 ** 2

    ssim_map = (2 * (mu1_mu2 + c1) * (2 * sigma_12 + c2)) / ((mu1_sq + mu2 + c1) * (sigma1_sq + sigma2_sq + c2))

    if size_average:
        return ssim_map.mean()
    else:
        return ssim_map.mean(1).mean(1).mean(1)


class SSIM(torch.nn.Module):
    def __init__(self, window_size=11, channel=1, size_average=True):
        super(SSIM, self).__init__()
        self.window_size = window_size
        self.size_average = size_average
        self.channel = channel
        self.window = create_window(window_size, channel)

    def forward(self, img1, img2):
        (_, channel, _, _) = img1.size()

        if channel == self.channel and self.window.data.type() == img1.data.type():
            window = self.window
        else:
            window = create_window(self.window_size, channel)
            if img1.is_cuda:
                window.cuda(img1.get_device())
            window = window.type_as(img1)
            self.window = window
            self.channel = channel

        return ssim(img1, img2, self.window, self.window_size, channel, self.size_average)


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
myssim = SSIM()

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
            npImg_a = cv2.imread(os.path.join(a_folder, a_dict[number]))
            npImg_b = cv2.imread(os.path.join(b_folder, b_dict[number]))

            img_a = torch.from_numpy(np.rollaxis(npImg_a, 2)).float().unsqueeze(0) / 255.0
            img_b = torch.from_numpy(np.rollaxis(npImg_b, 2)).float().unsqueeze(0) / 255.0

            if torch.cuda.is_available():
                img_a = img_a.cuda()
                img_b = img_b.cuda()

            img_a = Variable(img_a, requires_grad=False)
            img_b = Variable(img_b, requires_grad=True)

            a_init = img_a
            b_init = img_b
            continue
        a_next = os.path.join(a_folder, a_dict[number])
        b_next = os.path.join(b_folder, b_dict[number])

        npImg_a = cv2.imread(os.path.join(a_folder, a_dict[number]))
        npImg_b = cv2.imread(os.path.join(b_folder, b_dict[number]))

        img_a = torch.from_numpy(np.rollaxis(npImg_a, 2)).float().unsqueeze(0) / 255.0
        img_b = torch.from_numpy(np.rollaxis(npImg_b, 2)).float().unsqueeze(0) / 255.0

        if torch.cuda.is_available():
            img_a = img_a.cuda()
            img_b = img_b.cuda()

        img_a = Variable(img_a, requires_grad=False)
        img_b = Variable(img_b, requires_grad=True)

        a_next = img_a
        b_next = img_b
        # Functional: pytorch_ssim.ssim(img1, img2, window_size = 11, size_average = True)
        # ssim_value = pytorch_ssim.ssim(img_a, img_b).item()  ###
        score_a = myssim.forward(a_init, a_next)
        score_b = myssim.forward(b_init, b_next)
        # print("Initial ssim:", ssim_value)
        print("ours: ", score_a.item())
        print("Base: ", score_b.item())

        scores_a.append(score_a.item())
        scores_b.append(score_b.item())

        a_init = a_next
        b_init = b_next


        score_a_tmp = {p: scores_a}
        score_b_tmp = {p + "__base": scores_b}

        scores_dic[p] = scores_a
        scores_dic[p + "__base"] = scores_b

        data_a = pd.DataFrame(score_a_tmp)
        data_a.to_csv('C:/Users/user/PycharmProjects/landscapeDesign/llm/sim_ssim/sim_{}.csv'.format(p), index=False)

        data_b = pd.DataFrame(score_b_tmp)
        data_b.to_csv('C:/Users/user/PycharmProjects/landscapeDesign/llm/sim_ssim/sim_{}.csv'.format(p + "__base"), index=False)
data = pd.DataFrame(scores_dic)
data.to_csv('C:/Users/user/PycharmProjects/landscapeDesign/llm/sim_ssim/sim_total.csv', index=False)
