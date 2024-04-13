import random


def generate_random_scene():
    # Available objects and relationships
    available_objects = ["banya", "dogwood", "lily", "weep", "jap", "crepen", "tulip"]
    available_relationships = [["on the right of", "on the left of"],
                               ["in front of", "in behind of"]]

    # Randomly select 3 objects
    selected_objects = random.sample(available_objects, 3)

    # Randomly select 2 relationships and ensure unique pairings
    relations = []
    num = random.randint(0, 1)

    for i in range(2):
        while True:
            obj_a, obj_b = (selected_objects[i], selected_objects[i+1])
            relationship = random.choice(available_relationships[num])
            if (obj_a, relationship, obj_b) not in relations and (obj_b, relationship, obj_a) not in relations:
                relations.append((obj_a, relationship, obj_b))
                break
    return {
        "objects": selected_objects,
        "relationships": relations
    }
