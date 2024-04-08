import json


def get_default_scene_graph(file_path):
    # Load the content of the provided JSON file
    with open(file_path, "r") as file:
        data = json.load(file)

    # Placeholder for the formatted strings
    formatted_strings = []

    default_scene_graph_strings = []
    defaults_object_strings = []
    allows_object_strings = []

    # Iterate through each entry in the data
    for entry in data:
        # Extract required data
        caption = entry['Caption']
        scene_graph_objects = entry['Scene Graph']['objects']
        scene_graph_relationships = entry['Scene Graph']['relationships']
        background_prompt = entry['Background prompt']
        objects = entry['Objects']

        # Format the data into the desired string format
        formatted_caption = (
            f'Caption: {caption}\n'
            f'Scene Graph: {{"objects": {scene_graph_objects}, "relationships": {scene_graph_relationships}}}\n'
            f'Background prompt.txt: {background_prompt}'
        )

        formatted_scene_graph = (
            f'Scene Graph: {{"objects": {scene_graph_objects}, "relationships": {scene_graph_relationships}}}\n'
            f'Objects: {objects}'
        )

        # formatted_all = (
        #     f'Caption: {caption}\n'
        #     f'Objects: {objects}\n'
        #     f'Background prompt.txt: {background_prompt}'
        # )

        # Append the formatted string to the list
        default_scene_graph_strings.append(formatted_caption)
        defaults_object_strings.append(formatted_scene_graph)
        # allows_object_strings.append(formatted_all)

    # Join all formatted strings with two new lines
    default_caption = "\n\n".join(default_scene_graph_strings)
    default_scene_graph = "\n\n".join(defaults_object_strings)
    # default_all = "\n\n".join(allows_object_strings)

    return default_caption, default_scene_graph


if __name__ == "__main__":
    # Usage example (uncomment the following lines to use):
    default_caption, default_scene_graph = get_default_scene_graph("Backend/data/train.json")
    print("Default Scene Graph:")
    print(default_caption)
    print("\nDefaults Object:")
    print(default_scene_graph)
    # print("\nAll Object:")
    # print(default_all)
