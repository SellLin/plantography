# Define aspect ratios and relative sizes
import itertools

aspect_ratios = {
    "banya": (4, 10),
    "dogwood": (2, 4),
    "lily": (7, 9),
    "weep": (4, 6),
    "jap": (3, 5),
    "crepen": (5, 7),
    "tulip": (6, 8)
}

relative_sizes = {
    "banya": 1,  # As a reference
    "dogwood": 0.9,
    "jap": 0.8,
    "weep": 0.7,
    "crepen": 0.6,
    "tulip": 0.5,
    "lily": 0.4,
}

relationships = {
    "on the right of": (-1, 0),
    "on the left of": (1, 0),
    "on the top of": (0, 1),
    "on the bottom of": (0, -1),
    "in front of": (0, 0),  # z-axis front
    "in behind of": (0, 0)  # z-axis behind
}

def check_aspect_ratio(obj_name, bbox):
    width, height = bbox[2], bbox[3]
    ratio_width, ratio_height = aspect_ratios[obj_name]
    return abs(width / height - ratio_width / ratio_height) < 0.05  # tolerance


def check_relative_size(obj_name, bbox, bounding_boxes):
    banya_height = bounding_boxes["banya"][3]
    expected_height = banya_height * relative_sizes[obj_name]
    return abs(bbox[3] - expected_height) < 0.01  # tolerance


def check_within_image(bbox):
    return bbox[0] >= 0 and bbox[1] >= 0 and (bbox[0] + bbox[2]) <= 512 and (bbox[1] + bbox[3]) <= 512


def check_no_overlap(bounding_boxes):
    for obj_a, bbox_a in bounding_boxes.items():
        for obj_b, bbox_b in bounding_boxes.items():
            if obj_a != obj_b:
                if (bbox_a[0] < bbox_b[0] + bbox_b[2] and bbox_a[0] + bbox_a[2] > bbox_b[0] and
                        bbox_a[1] < bbox_b[1] + bbox_b[3] and bbox_a[1] + bbox_a[3] > bbox_b[1]):
                    return False
    return True


def check_relationships(relations, bounding_boxes):
    er = []
    for obj_name, bbox in bounding_boxes.items():
        if not check_aspect_ratio(obj_name, bbox):
            print(f"Aspect ratio of {obj_name} is incorrect.")
            er.append(1)

    relation_dict = {(subj, obj): relation for subj, relation, obj in relations}
    for subj, obj in relation_dict:
        relation = relation_dict[(subj, obj)]
        dx, dy = relationships[relation]

        subj_center_x = bounding_boxes[subj][0] + bounding_boxes[subj][2] / 2
        subj_center_y = bounding_boxes[subj][1] + bounding_boxes[subj][3] / 2

        obj_center_x = bounding_boxes[obj][0] + bounding_boxes[obj][2] / 2
        obj_center_y = bounding_boxes[obj][1] + bounding_boxes[obj][3] / 2

        if dx != 0:
            # Check horizontal relationships based on center points
            if (subj_center_x - obj_center_x) * dx > 0:
                print(f"{subj} is not {relation} {obj}.")
                er.append(2)

        if dy != 0:
            # Check vertical relationships based on center points
            if (subj_center_y - obj_center_y) * dy > 0:
                print(f"{subj} is not {relation} {obj}.")
                er.append(2)

    for subj, obj in relation_dict:
        relation = relation_dict[(subj, obj)]
        # For front and behind relationships, let's check size considering relative sizes
        if relation == "in front of":
            obj_expected_height = bounding_boxes[subj][3] * (relative_sizes[obj] / relative_sizes[subj])
            if bounding_boxes[obj][3] > obj_expected_height:
                print(f"{subj} is not {relation} {obj}.")
                er.append(3)

        if relation == "in behind of":
            obj_expected_height = bounding_boxes[subj][3] * (relative_sizes[obj] / relative_sizes[subj])
            if bounding_boxes[obj][3] < obj_expected_height:
                print(f"{subj} is not {relation} {obj}.")
                er.append(3)

    for subj, obj in relation_dict:
        relation = relation_dict[(subj, obj)]
        if relation not in ["in front of", "in behind of"]:  # Check relative sizes for other relationships
            print("aaa:", abs((bounding_boxes[subj][3] / relative_sizes[subj]) / (bounding_boxes[obj][3] / relative_sizes[obj]) - 1))
            if abs((bounding_boxes[subj][3] / relative_sizes[subj]) /
                   (bounding_boxes[obj][3] / relative_sizes[obj]) - 1) > 0.05:
                # print(abs(subj_actual_relative_size - relative_sizes[subj] / relative_sizes[obj]))
                # if abs(subj_actual_relative_size - relative_sizes[subj] / relative_sizes[obj]) > 0.1: # tolerance for minor variations
                print(f"{subj} is not same size with {relation} {obj}.")
                er.append(4)
    er.append(0)
    return er


def check_bbox(scene, bounding_boxes):
    relations = scene["relationships"]
    # relations = [
    #     (scene['objects'][scene['relationships'][0][0]], scene['relationships'][0][1],
    #      scene['objects'][scene['relationships'][0][2]]),
    #     (scene['objects'][scene['relationships'][1][0]], scene['relationships'][1][1],
    #      scene['objects'][scene['relationships'][1][2]]),
    # ]
    # relations = [
    #     # Example relationships. This should be populated based on your scene graph.
    #     ("banya", "on the right of", "dogwood"),
    #     ("banya", "in front of", "dogwood"),
    #     # Add more as needed...
    # ]

        # if not check_relative_size(obj_name, bbox):
        #     print(f"Relative size of {obj_name} is incorrect.")
        #     return False

        # if not check_within_image(bbox):
        #     print(f"{obj_name} is not within the image boundaries.")
        #     return 5

    # if not check_no_overlap():
    #     print("Some bounding boxes overlap.")
    #     return False
    return check_relationships(relations, bounding_boxes)
