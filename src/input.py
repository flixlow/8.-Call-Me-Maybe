import json


def open_json_file_to_list(file_name: str) -> list:
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data


if __name__ == "__main__":
    data = open_json_file_to_list("data/input/functions_definition.json")
    print(data)
