'''
You are an expert in bounding box generation.

Giving you a scene graph and a set of generation rules, your task is to generate bounding box for each object in the given scene graph based on the spatial relation descripted in scene graph and generation rules. Each bounding box should be in the format of (object name, [top -left x coordinate, top -left y coordinate, box width, box height]) and include exactly one object.
The images are of size 512x512, and the bounding boxes should not overlap or go beyond the image boundaries.The first plant height initial set to 100.


Your task should be done in two steps.
Step 1: Determine the position of each object based on scene graph. From left to right, the x position decreases.
Step 2: Determine the size of each object based on the aspect ratio rule and relative size rule.
Step 3: Adjust the size of each object based on the scaling rule. (determine the distance relationship between objects, then scale the object behind)
Aspect ratio rule:
1. Banya have aspect ratio as 4:10
2. Dogwood have aspect ratio as 2:4
3. Jap have aspect ratio as 3:5
4. Weep have aspect ratio as 4:6
5. Crepen have aspect ratio as 5:7
6. Tulip have aspect ratio as 6:8
7. Lily have aspect ratio as 7:9

Relative size rule:
1. The height of banya is 1
1. The height of dogwood is 0.9
2. The height of jap is 0.8
3. The height of weep is 0.7
4. The height of crepen is 0.6
5. The height of tulip is 0.5
6. The height of lily is 0.4

Scaling rule:
If there is relation that present the front and back relation, such as [a, in front of, b], the size between a and b should have a scaling relation. The object behind should scale the width and height smaller than before, keeping the aspect ratio.
Only the object in relation as [a, in front of, b] or [a, in behind of, b] can be scaled. When scaling the object behind, if the object in front is already scaled, the scaling retio should increase a little after each scaling.

Below shows an example for you:
Description:
"""
'objects': ['dogwood', 'lily', 'tulip', 'weep']
'relationships': [('dogwood', 'in front of', 'lily'), ('lily', 'on the left of', 'tulip'), ('lily', 'on the right of', 'weep')]
"""
Generation:
"""
Step 1: Determine the position of each object based on the scene graph.
Based on the given scene graph, we can determine the position of each object as follows:
Dogwood is in front of Lily.
Lily is on the left of Tulip, so lily's x position is less than Tulip's x position.
Lily is on the right of Weep, so lily's x position is lager than Weep's x position.
So distance from left to right is (Weep, 64) < (Lily, 128) < (Tulip, 384)
We can assign initial positions as follows:
Dogwood: (256, 256)
Weep: (64, 256)
Lily: (128, 256) 
Tulip: (384, 256)
Since Lily is on the right of Weep, Lily's x position is lager than Weep's x position. So, Lily's x position is set to 128, and Weep's x position is set to 64, as Weep's x position:128>Lily's x position:64.
Since Lily is on the left of Tulip, Lily's x position is less than Tulip's x position. So, Lily's x position is set to 128, and Tulip's x position is set to 384, as Lily's x position:128<Tulip's x position:384.
Step 2: Determine the size of each object based on the aspect ratio rule and relative size rule.
The first plant height is initially set to 100. Based on the given aspect ratio and relative size rules, we can determine the size of each object as follows:
Tulip: height = 100 * 0.5 = 50, width = (50 * 6) / 8 = 37.5
Dogwood: height = 100 * 0.9 = 90, width = (90 * 2) / 4 = 45
Lily: height = 100 * 0.4 = 40, width = (40 * 7) / 9 = 31.1
Weep: height = 100 * 0.7 = 70, width = (70 * 4) / 6 = 46.7

Step 3: Adjust the size of each object based on the scaling rule.
Since Dogwood is in front of Lily, distance from front to back is Dogwood > Lily.
So we should scale Lily's width and height smaller.
Lily (scaled): height = 40 * 0.9 = 36, width = 31.1 * 0.9 = 28


Bounding boxes generated:
"bbox": {
"dogwood": [256, 256, 45, 90],
"lily": [128, 256, 28, 36],
"tulip": [384, 256, 37.5, 50],
"weep": [64, 256, 46.7, 70]
}
"""

Description:
"""
'objects' ['tulip', 'dogwood', 'weep']
'relationships' [('tulip', 'in behind of', 'dogwood'), ('dogwood', 'in front of', 'weep')]
"""

Generation:
"""
Step 1 Determine the position of each object based on the scene graph.
Based on the given scene graph, we can determine the position of each object as follows
Tulip is in behind of Dogwood.
Dogwood is in front of Weep.

We can assign initial positions as follows
Tulip (256, 256)
Dogwood (128, 256)
Weep (384, 256)

Since Tulip is in behind of Dogwood, there is no restriction on x position.
Since Dogwood is in front of Weep, there is no restriction on x position.

Step 2 Determine the size of each object based on the aspect ratio rule and relative size rule.
The first plant height is initially set to 100. Based on the given aspect ratio and relative size rules, we can determine the size of each object as follows
Tulip height = 100  0.5 = 50, width = (50  6)  8 = 37.5
Dogwood height = 100  0.9 = 90, width = (90  2)  4 = 45
Weep height = 100  0.7 = 70, width = (70  4)  6 = 46.7

Step 3 Adjust the size of each object based on the scaling rule.
Since Tulip is in behind of Dogwood and Dogwood is in front of Weep, we judge distance is Dogwood > Tulip == Weep.
So, we should scale Tulip and Weep's width and height smaller.
Tulip (scaled) height = 50  0.9 = 45, width = 37.5  0.9 = 33.75
Weep (scaled) height = 70  0.9 = 63, width = 46.7  0.9 = 42.03


Bounding boxes generated
bbox {
tulip [128, 256, 33.75, 45],
dogwood [256, 256, 45, 90],
weep [384, 256, 42.03, 63]
}
"""

Description:
"""
'objects': ['banya', 'jap', 'dogwood']
'relationships': [('banya', 'in behind of', 'jap'), ('jap', 'in front of', 'dogwood')]
"""

Generation:
"""
Step 1: Determine the position of each object based on the scene graph.
Based on the given scene graph, we can determine the position of each object as follows:
Banya is in behind of Jap.
Jap is in front of Dogwood.

We can assign initial positions as follows:
Banya: (128, 256)
Jap: (256, 256)
Dogwood: (384, 256)

Since Banya is in behind of Jap, there is no restriction on x position.
Since Jap is in front of Dogwood, there is no restriction on x position.

Step 2: Determine the size of each object based on the aspect ratio rule and relative size rule.
The first plant height is initially set to 100. Based on the given aspect ratio and relative size rules, we can determine the size of each object as follows:
Banya: height = 100 * 1 = 100, width = (100 * 4) / 10 = 40
Jap: height = 100 * 0.8 = 80, width = (80 * 3) / 5 = 48
Dogwood: height = 100 * 0.9 = 90, width = (90 * 2) / 4 = 45

Step 3: Adjust the size of each object based on the scaling rule.
Since Banya is in behind of Jap and Jap is in front of Dogwood, we judge distance is Jap > Banya == Dogwood.
So, we should scale Banya and Dogwood's width and height smaller.
Banya (scaled): height = 100 * 0.9 = 90, width = 40 * 0.9 = 36
Dogwood (scaled): height = 90 * 0.9 = 81, width = 45 * 0.9 = 40.5


Bounding boxes generated:
"bbox": {
"banya": [128, 256, 36, 90],
"jap": [256, 256, 48, 80],
"dogwood": [384, 256, 40.5, 81]
}
"""

Description:
"""
'objects': ['tulip', 'lily', 'crepen']
'relationships': [('tulip', 'on the left of', 'lily'), ('lily', 'on the right of', 'crepen')]
"""

Generation:
"""
Step 1: Determine the position of each object based on the scene graph.
Based on the given scene graph, we can determine the position of each object as follows:
Tulip is on the left of Lily.
Lily is on the right of Crepen.
So distance from left to right is (Tulip,128) < (Lily, 384) and (Crepen,256) < (Lily, 384)
We can assign initial positions as follows:
Tulip: (128, 256)
Crepen: (256, 256)
Lily: (384, 256)
Since Tulip is on the left of Lily, Tulip's x position is less than Lily's x position. So, Tulip's x position is set to 128, and Lily's x position is set to 384, as Tulip's x position:128<Lily's x position:384
Since Lily is on the right of Crepen, Lily's x position is larger than Crepen's x position. So, Lily's x position is set to 384, and Crepen's x position is set to 256, as Lily's x position:384>Crepen's x position:256.

Step 2: Determine the size of each object based on the aspect ratio rule and relative size rule.
The first plant height is initially set to 100. Based on the given aspect ratio and relative size rules, we can determine the size of each object as follows:
Tulip: height = 100 * 0.5 = 50, width = (50 * 6) / 8 = 37.5
Lily: height = 100 * 0.4 = 40, width = (40 * 7) / 9 = 31.1
Crepen: height = 100 * 0.6 = 60, width = (60 * 5) / 7 = 42.9

Step 3: Adjust the size of each object based on the scaling rule.
Since there is no front or in behind relationship present in the scene graph, we do not need to scale any object.

Bounding boxes generated:
"bbox": {
"tulip": [128, 256, 37.5, 50],
"lily": [256, 256, 31.1, 40],
"crepen": [384, 256, 42.9, 60]
}
"""

Description:
"""
'objects': ['dogwood', 'weep', 'crepen']
'relationships': [('dogwood', 'in front of', 'weep'), ('weep', 'in behind of', 'crepen')]
"""

Generation:
"""
Step 1: Determine the position of each object based on the scene graph.
Based on the given scene graph, we can determine the position of each object as follows:
Dogwood is in front of Weep.
Weep is in behind of Crepen.

We can assign initial positions as follows:
Dogwood: (128, 256)
Weep: (256, 256)
Crepen: (384, 256)

Since Dogwood is in front of Weep and Weep is in behind of Crepen, there is no restriction on x position.

Step 2: Determine the size of each object based on the aspect ratio rule and relative size rule.
The first plant height is initially set to 100. Based on the given aspect ratio and relative size rules, we can determine the size of each object as follows:
Dogwood: height = 100 * 0.9 = 90, width = (90 * 2) / 4 = 45
Weep: height = 100 * 0.7 = 70, width = (70 * 4) / 6 = 46.7
Crepen: height = 100 * 0.6 = 60, width = (60 * 5) / 7 = 42.9

Step 3: Adjust the size of each object based on the scaling rule.
Since Dogwood is in front of Weep and Weep is in behind of Crepen, we judge distance is Dogwood == Crepen > Weep.
So, we should scale Weep and Crepen's width and height smaller.
Weep (scaled): height = 70 * 0.9 = 63, width = 46.7 * 0.9 = 42.03


Bounding boxes generated:
"bbox": {
"dogwood": [128, 256, 45, 90],
"weep": [256, 256, 42.03, 63],
"crepen": [384, 256, 42.9, 60]
}
"""


Input scene graph:
'''

###########################################################################################







prompts = '''
You are an expert in bounding box generation.

Giving you a scene graph and a set of generation rules, your task is to generate bounding box for each object in the given scene graph based on the spatial relation descripted in scene graph and generation rules. Each bounding box should be in the format of (object name, [top -left x coordinate, top -left y coordinate, box width, box height]) and include exactly one object.
The images are of size 512x512, and the bounding boxes should not overlap or go beyond the image boundaries.The first plant height initial set to 100.


Your task should be done in two steps.
Step 1: Determine the position of each object based on scene graph. From left to right, the x position decreases.
Step 2: Determine the size of each object based on the aspect ratio rule and relative size rule.
Step 3: Adjust the size of each object based on the scaling rule. (determine the distance relationship between objects, then scale the object behind)
Aspect ratio rule:
1. Banya have aspect ratio as 4:10
2. Dogwood have aspect ratio as 2:4
3. Jap have aspect ratio as 3:5
4. Weep have aspect ratio as 4:6
5. Crepen have aspect ratio as 5:7
6. Tulip have aspect ratio as 6:8
7. Lily have aspect ratio as 7:9

Relative size rule:
1. The height of banya is 1
1. The height of dogwood is 0.9
2. The height of jap is 0.8
3. The height of weep is 0.7
4. The height of crepen is 0.6
5. The height of tulip is 0.5
6. The height of lily is 0.4

Scaling rule:
If there is relation that present the front and back relation, such as [a, in front of, b], the size between a and b should have a scaling relation. The object behind should scale the width and height smaller than before, keeping the aspect ratio.
Only the object in relation as [a, in front of, b] or [a, in behind of, b] can be scaled. When scaling the object behind, if the object in front is already scaled, the scaling retio should increase a little after each scaling.

The output format should be like below:
Bounding boxes generated:
"bbox": {
"dogwood": [128, 256, 45, 90],
"weep": [256, 256, 42.03, 63],
"crepen": [384, 256, 42.9, 60]
}
"""


Input scene graph:
'''




########################################################################

'''
You are an expert in bounding box generation.

Giving you a scene graph and a set of generation rules, your task is to generate bounding box for each object in the given scene graph based on the spatial relation descripted in scene graph and generation rules. Each bounding box should be in the format of (object name, [top -left x coordinate, top -left y coordinate, box width, box height]) and include exactly one object.
The images are of size 512x512, and the bounding boxes should not overlap or go beyond the image boundaries.The first plant height initial set to 100.


Your task should be done in two steps.
Step 1: Determine the position of each object based on scene graph. From left to right, the x position decreases.
Step 2: Determine the size of each object based on the aspect ratio of a plant should have and relative size between plants. For example, a normal tree should have height larger than width, and a tree normally larger than bush.
Step 3: Adjust the size of each object based on the perspective relation. The farther object should have smaller size.


The output format should be like below:
Bounding boxes generated:
"bbox": {
"dogwood": [128, 256, 45, 90],
"weep": [256, 256, 42.03, 63],
"crepen": [384, 256, 42.9, 60]
}
"""


Input scene graph:
'''








































##################################################################################################
'''
You are an expert in bounding box generation.

Giving you a scene graph and a set of generation rules, your task is to generate bounding box for each object in the given scene graph based on the spatial relation descripted in scene graph and generation rules. Each bounding box should be in the format of (object name, [top -left x coordinate, top -left y coordinate, box width, box height]) and include exactly one object.
The images are of size 512x512, and the bounding boxes should not overlap or go beyond the image boundaries.The first plant height initial set to 100.

Your task should be done in two steps.
Step 1: generate bounding box based on scene graph.
Step 2: Explain the size of each bounding box that is generated based on three rules, in a ordering[1. aspect ratio rule, 2. relative size rule and 3. scaling rule]. The generation rules are given below:
Aspect ratio rule:
1. Banya have aspect ratio as 4:10
2. Dogwood have aspect ratio as 2:4 
3. Jap have aspect ratio as 3:5
4. Weep have aspect ratio as 4:6
5. Crepen have aspect ratio as 5:7
6. Tulip have aspect ratio as 6:8
7. Lily have aspect ratio as 7:9

Relative size rule:
1. The height of dogwood is twice as high as banya
2. The height of dogwood is 1.5 times as high as jap
3. The height of dogwood is 1.6 times as high as weep
4. The height of dogwood is 1.7 times as high as crepen
5. The height of dogwood is 3.1 times as high as tulip
6. The height of dogwood is 3.5 times as high as lily

Scaling rule:
If there is relation that present the front and back relation, such as [a, in front of, b], the size between a and b should have a scaling relation. The object behind should scale the width and height smaller than before, keeping the aspect ratio.


Below shows an example for you:
Description: 
"""
"objects": ["banya", "dogwood"]
"relationships": [0, "on the right of", 1], [0, "in front of", 1]
"""
Generation:
"""
Step 1: Generate bounding box based on scene graph

Place the banya in the image with its aspect ratio of 4:10 and the dogwood with its aspect ratio of 2:4.
Since the dogwood's height is twice as high as the banya, set the banya's height to 100 and its width to 40 (based on the aspect ratio), and the dogwood's height to 200 and width to 100.
Place the banya at the coordinates (100, 206) to have it within the image boundaries.
Since the banya is on the right of the dogwood and in front of the dogwood, place the dogwood at the coordinates (0, 156).
Scaling rule: Since the banya is in front of the dogwood, the dogwood's width and height should be scaled down while keeping the aspect ratio. Since the scaling factor is not specified, we will assume a scaling factor of 0.9. So, the scaled down dimensions of the dogwood are 180 (height) and 90 (width).
Step 2: Explain the size of each bounding box based on generation rules

Aspect ratio rule:

Banya: Height = 100, Width = 40 (aspect ratio 4:10)
Dogwood: Height = 200, Width = 100 (aspect ratio 2:4)
Relative size rule:

Dogwood's height (200) is twice as high as Banya's height (100)
Scaling rule:

Dogwood is behind Banya, so it's scaled down to 180 (height) and 90 (width), keeping the aspect ratio.

Bounding boxes generated:
"bbox": {
"banya": [100, 206, 40, 100],
"dogwood": [0, 156, 90, 180]
}
"""

Input scene graph:
'''


def get_prompts(scene):
    return prompts + '"objects": ' + str(scene["objects"]) + ']\n"relationships: ' + str(scene["relationships"])
