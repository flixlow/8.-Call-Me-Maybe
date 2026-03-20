from argparse import ArgumentParser, Namespace
import json


def open_json_file_to_list(file_name: str) -> list:
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data


def parser() -> Namespace:
    parser = ArgumentParser()

    flags = ["--functions_definition",
             "--input",
             "--output"]

    default_files = ["data/input/functions_definition.json",
                     "data/input/function_calling_tests.json",
                     "data/output/function_calls.json"]

    for flag, default_file in zip(flags, default_files):
        parser.add_argument(flag, default=default_file)

    return parser.parse_args()


if __name__ == "__main__":
    parsing = parser()
    print(parsing.functions_definition)
    print(parsing.input)
    print(parsing.output)
    data = open_json_file_to_list("data/input/functions_definition.json")
    print(data)
