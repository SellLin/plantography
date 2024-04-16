import pandas as pd
import json


# Function to check if a value can be converted to an integer
def is_convertible_to_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


# Function to convert the Scene Graph string to a JSON object
def parse_scene_graph(scene_graph):
    """Fix the JSON format and return a proper JSON object."""
    try:
        # Enclose the string with curly braces
        json_str = "{" + scene_graph + "}"
        # Replace single quotes with double quotes
        fixed_str = json_str.replace("'", '"')
        return json.loads(fixed_str)
    except json.JSONDecodeError:
        return {}


# Function to create an entry for an image
def create_entry(row, boundingbox, default_caption):
    scene_graph = parse_scene_graph(row['Scenegraph'])
    bg = default_caption.split("\n")[-1].replace("Background prompt.txt:", "").strip()
    entry = {
        "Image_id": row['image_name'],
        "Caption": row['Description'].replace("\n", " ").rstrip(),
        "Scene Graph": scene_graph,
        "Objects": [],
        "Background prompt.txt": bg
    }
    bboxes = boundingbox[boundingbox['image_name'] == row['image_name']]
    for _, bbox_row in bboxes.iterrows():
        entry["Objects"].append((bbox_row['label_name'],
                                 [int(bbox_row['bbox_x']) if is_convertible_to_int(bbox_row['bbox_x']) else None,
                                  int(bbox_row['bbox_y']) if is_convertible_to_int(bbox_row['bbox_y']) else None,
                                  int(bbox_row['bbox_width']) if is_convertible_to_int(
                                      bbox_row['bbox_width']) else None,
                                  int(bbox_row['bbox_height']) if is_convertible_to_int(
                                      bbox_row['bbox_height']) else None]))

    return entry


def generate_structured_format(row):
    caption = row['Description'].replace("\n", "")
    scenegraph = row['Scenegraph'].replace("\n", "")
    bg_prompt = "A picture of a real landscape."
    return {
        "Caption": caption,
        "Scene Graph": scenegraph,
        "Background prompt.txt": bg_prompt
    }


if __name__ == "__main__":
    # Load the CSV files
    description_df = pd.read_csv('data/Description_SG_0815.csv')
    boundingbox_df = pd.read_csv('data/boundingbox_0815.csv')

    # Define a Function to Generate the Structured Format
    structured_data = description_df.apply(generate_structured_format, axis=1).tolist()
    output_df = pd.DataFrame(structured_data)
    output_df['image_name'] = description_df['image_name']

    # Get the default caption and selected images
    random_samples = output_df.sample(n=10)
    images_10 = []
    entries = []
    for _, row in random_samples.iterrows():
        images_10.append(row['image_name'])
        entry = f"Caption: {row['Caption']} \nScene Graph: {row['Scene Graph']} \nBackground prompt.txt: {row['Background prompt.txt']}"
        entries.append(entry)
    default_caption = "\n\n".join(entries)
    # print(default_caption)

    # Splitting the data
    train_df = description_df[description_df['image_name'].isin(images_10)]
    test_df = description_df[~description_df['image_name'].isin(images_10)]
    # print(test_df)

    # Create dictionaries for training and test sets
    train_entries = [create_entry(row, boundingbox_df, default_caption) for _, row in train_df.iterrows()]
    test_entries = [create_entry(row, boundingbox_df, default_caption) for _, row in test_df.iterrows()]

    # Construct the string representation
    default_scene_graph_parts = []

    for entry in train_entries:
        scene_graph_str = "Scene Graph: " + json.dumps(entry["Scene Graph"])
        objects_str = "Objects: " + str(entry["Objects"]) + "\n"
        default_scene_graph_parts.extend([scene_graph_str, objects_str])

    # for entry in test_entries:
    #     print(entry["Image_id"])
    #     print(entry["Caption"])
    #     print(entry["Scene Graph"])
    #     print(entry["Objects"])
    #     print(entry["Background prompt.txt"])
    #     print("\n")

    # Combine the parts into the final default_scene_graph string
    default_scene_graph = "\n".join(default_scene_graph_parts)

    # print(default_scene_graph)

    # Write the dictionaries to train.json and test.json
    # with open('data/train.json', 'w') as train_file:
    #     json.dump(train_entries, train_file, indent=2)
    #     print("train.json created")
    #
    # with open('data/test.json', 'w') as test_file:
    #     json.dump(test_entries, test_file, indent=2)
    #     print("test.json created")
