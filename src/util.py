import json
import os


def write_local_json(file_name, data):
    """Writes a json file in data folder.

    :param file_name: Name of file to be written
    :param data: Data to be written to file

    """
    with open(os.path.join('data', file_name + '.json'), 'w') as json_file:
        json.dump(data, json_file)


def read_local_json(file_name):
    """Reads a json file in data folder.

    :param file_name: Name of file to be read from

    """
    with open(os.path.join('data', file_name + '.json'), 'r') as json_file:
        return json.load(json_file)
