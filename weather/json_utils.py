import json


def load_json(file_path):
    """
    Load JSON data from a file.

    Args:
        file_path (str or Path): Path to the JSON file.

    Returns:
        dict or list: Parsed JSON data.

    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    return data


def append_to_json(file_path, new_data):
    """
        Append new data to the JSON file.

        Args:
            file_path (str): The path to the JSON file.
            new_data (dict): The new data to append (key-value pairs).
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

        data.update(new_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
