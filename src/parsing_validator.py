from pydantic import TypeAdapter
from argparse import ArgumentParser, Namespace
from src.utils_class import Prompt, Func
import json


def open_json_file_to_list(file_name: str) -> list:
    """
    Open a JSON file and return its content as a list.

    Args:
        file_name (str): Path to the JSON file.

    Returns:
        list: Content of the JSON file.
    """
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data


def parsing() -> Namespace:
    """
    Parse command-line arguments for input/output files.

    Returns:
        Namespace: Parsed arguments.
    """
    parser = ArgumentParser()

    flags = ["--functions_definition",
             "--input",
             "--output"]

    default_files = ["data/input/functions_definition.json",
                     "data/input/function_calling_tests.json",
                     "data/output/function_calling_results.json"]

    for flag, default_file in zip(flags, default_files):
        parser.add_argument(flag, default=default_file)

    return parser.parse_args()


def parse_and_check_args_and_files() -> tuple[
        Namespace, list[Func], list[Prompt]]:
    """
    Parse arguments and validate input files to get functions and prompts.

    Returns:
        tuple: (parser, validated functions, validated prompts)
    """
    parser = parsing()

    functions = open_json_file_to_list(parser.functions_definition)
    prompts = open_json_file_to_list(parser.input)

    func_validator = TypeAdapter(list[Func])
    prompt_validator = TypeAdapter(list[Prompt])

    validated_functions = func_validator.validate_python(functions)
    validated_prompts = prompt_validator.validate_python(prompts)

    return (parser, validated_functions, validated_prompts)


if __name__ == "__main__":
    parser, functions, prompts = parse_and_check_args_and_files()
    print(parser)
    print(functions)
    print(prompts)
