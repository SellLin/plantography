default_template = """You are an intelligent bounding box generator. I will provide you with a caption for a photo, image, or painting. Your task is to generate the bounding boxes for the objects mentioned in the caption, along with a background prompt describing the scene. The images are of size 512x512. The top-left corner has coordinate [0, 0]. The bottom-right corner has coordinnate [512, 512]. The bounding boxes should not overlap or go beyond the image boundaries. Each bounding box should be in the format of (object name, [top-left x coordinate, top-left y coordinate, box width, box height]) and include exactly one object (i.e., start the object name with "a" or "an" if possible). Do not put objects that are already provided in the bounding boxes into the background prompt. Do not include non-existing or excluded objects in the background prompt. If needed, you can make reasonable guesses. Please refer to the example below for the desired format.

Caption: A realistic image of landscape scene depicting a green car parking on the left of a blue truck, with a red air balloon and a bird in the sky
Objects: [('a green car', [21, 281, 211, 159]), ('a blue truck', [269, 283, 209, 160]), ('a red air balloon', [66, 8, 145, 135]), ('a bird', [296, 42, 143, 100])]
Background prompt: A realistic landscape scene
Negative prompt: 

Caption: A realistic top-down view of a wooden table with two apples on it
Objects: [('a wooden table', [20, 148, 472, 216]), ('an apple', [150, 226, 100, 100]), ('an apple', [280, 226, 100, 100])]
Background prompt: A realistic top-down view
Negative prompt: 

Caption: A realistic scene of three skiers standing in a line on the snow near a palm tree
Objects: [('a skier', [5, 152, 139, 168]), ('a skier', [278, 192, 121, 158]), ('a skier', [148, 173, 124, 155]), ('a palm tree', [404, 105, 103, 251])]
Background prompt: A realistic outdoor scene with snow
Negative prompt: 

Caption: An oil painting of a pink dolphin jumping on the left of a steam boat on the sea
Objects: [('a steam boat', [232, 225, 257, 149]), ('a jumping pink dolphin', [21, 249, 189, 123])]
Background prompt: An oil painting of the sea
Negative prompt: 

Caption: A cute cat and an angry dog without birds
Objects: [('a cute cat', [51, 67, 271, 324]), ('an angry dog', [302, 119, 211, 228])]
Background prompt: A realistic scene
Negative prompt: birds

Caption: Two pandas in a forest without flowers
Objects: [('a panda', [30, 171, 212, 226]), ('a panda', [264, 173, 222, 221])]
Background prompt: A forest
Negative prompt: flowers

Caption: 一个客厅场景的油画，墙上挂着一幅画，电视下面是一个柜子，柜子上有一个花瓶，画里没有椅子。
Objects: [('a painting', [88, 85, 335, 203]), ('a cabinet', [57, 308, 404, 201]), ('a flower vase', [166, 222, 92, 108]), ('a flower vase', [328, 222, 92, 108])]
Background prompt: An oil painting of a living room scene
Negative prompt: chairs"""

simplified_prompt = """{template}

Caption: {prompt}
Objects: """

stage1_examples = [
    ["""A realistic photo of a wooden table with an apple on the left and a pear on the right."""],
    ["""A realistic photo of 4 TVs on a wall."""],
    ["""A realistic photo of a gray cat and an orange dog on the grass."""],
    ["""In an empty indoor scene, a blue cube directly above a red cube with a vase on the left of them."""],
    ["""A realistic photo of a wooden table without bananas in an indoor scene"""],
    ["""A realistic photo of two cars on the road."""],
    ["""一个室内场景的水彩画，一个桌子上面放着一盘水果"""]
]

# Layout, seed
stage2_examples = [
    ["""Caption: A realistic top-down view of a wooden table with an apple on the left and a pear on the right.
Objects: [('a wooden table', [30, 30, 452, 452]), ('an apple', [52, 223, 50, 60]), ('a pear', [400, 240, 50, 60])]
Background prompt: A realistic top-down view of a room""", "A realistic top-down view of a wooden table with an apple on the left and a pear on the right.", 0],
    ["""Caption: A realistic photo of 4 TVs on a wall.
Objects: [('a TV', [12, 108, 120, 100]), ('a TV', [132, 112, 120, 100]), ('a TV', [252, 104, 120, 100]), ('a TV', [372, 106, 120, 100])]
Background prompt: A realistic photo of a wall""", "A realistic photo of 4 TVs on a wall.", 0],
    ["""Caption: A realistic photo of a gray cat and an orange dog on the grass.
Objects: [('a gray cat', [67, 243, 120, 126]), ('an orange dog', [265, 193, 190, 210])]
Background prompt: A realistic photo of a grassy area.""", "A realistic photo of a gray cat and an orange dog on the grass.", 0],
    ["""Caption: 一个室内场景的水彩画，一个桌子上面放着一盘水果
Objects: [('a table', [81, 242, 350, 210]), ('a plate of fruits', [151, 287, 210, 117])]
Background prompt: A watercolor painting of an indoor scene""", "", 1],
    ["""Caption: In an empty indoor scene, a blue cube directly above a red cube with a vase on the left of them.
Objects: [('a blue cube', [232, 116, 76, 76]), ('a red cube', [232, 212, 76, 76]), ('a vase', [100, 198, 62, 144])]
Background prompt: An empty indoor scene""", "In an empty indoor scene, a blue cube directly above a red cube with a vase on the left of them.", 2],
    ["""Caption: A realistic photo of a wooden table without bananas in an indoor scene
Objects: [('a wooden table', [75, 256, 365, 156])]
Background prompt: A realistic photo of an indoor scene
Negative prompt: bananas""", "A realistic photo of a wooden table without bananas in an indoor scene", 3],
    ["""Caption: A realistic photo of two cars on the road.
Objects: [('a car', [20, 242, 235, 185]), ('a car', [275, 246, 215, 180])]
Background prompt: A realistic photo of a road.""", "A realistic photo of two cars on the road.", 4],
]


prompt_placeholder = "A realistic photo of a gray cat and an orange dog on the grass."

layout_placeholder = """Caption: A realistic photo of a gray cat and an orange dog on the grass.
Objects: [('a gray cat', [67, 243, 120, 126]), ('an orange dog', [265, 193, 190, 210])]
Background prompt: A realistic photo of a grassy area."""
