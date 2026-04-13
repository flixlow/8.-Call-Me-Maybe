import json
from typing import Any
from pydantic import TypeAdapter, ValidationError
from argparse import ArgumentParser, Namespace
from src.utils_classes import Prompt, Func
from src.custom_errors import FileOpeningError, ArgumentError
from src.custom_errors import FunctionError, PromptError


def open_json_file_to_list(file_name: str) -> list[dict[str, Any]]:
    """Open a JSON file and return its content as a list.

    Args:
        file_name (str): Path to the JSON file.

    Returns:
        list: Content of the JSON file.
    """
    try:
        with open(file_name) as json_file:
            data: list[dict[str, Any]] = json.load(json_file)
        return data
    except FileNotFoundError:
        raise FileOpeningError(
            f"\nInput file not found: '{file_name}'"
            f"\nPlease check the path and ensure the file exists.")
    except json.JSONDecodeError as e:
        raise FileOpeningError(f"\nInvalid JSON in '{file_name}'."
                               f"\nError at line {e.lineno}")
    except PermissionError:
        raise FileOpeningError(
            f"Permission denied when reading '{file_name}'.\n")
    except Exception as e:
        raise FileOpeningError(f"Error reading '{file_name}': {e}")


def parsing() -> Namespace:
    """Parse command-line arguments for input/output files.

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

    parser.add_argument("--interactive", action='store_true')

    return parser.parse_args()


def parse_and_check_args_and_files() -> tuple[
        Namespace, list[Func], list[Prompt]]:
    """Parse arguments and validate input files to get functions and prompts.

    Returns:
        tuple: (parser, validated functions, validated prompts)
    """
    try:
        parser = parsing()
    except SystemExit:
        raise ArgumentError() from None

    functions = open_json_file_to_list(parser.functions_definition)
    prompts = open_json_file_to_list(parser.input)

    if functions == []:
        raise FunctionError("\nThe list of functions in "
                            f"{parser.functions_definition} is empty.")

    if prompts == []:
        raise PromptError(
            f"\nThe list of prompts in {parser.input} is empty.")

    func_validator = TypeAdapter(list[Func])
    prompt_validator = TypeAdapter(list[Prompt])

    try:
        validated_functions = func_validator.validate_python(functions)
    except ValidationError as e:
        err = e.errors()[0]
        message = (f"\nLOCALISATION: {err['loc']}"
                   "\nUNVALID FUNCTION: "
                   f"{json.dumps(err['input'], indent=4)}")
        raise FunctionError(message) from e

    try:
        validated_prompts = prompt_validator.validate_python(prompts)
    except ValidationError as e:
        err = e.errors()[0]
        if err['type'] == "value_error":
            raise PromptError(f"\n{err['msg'].split(", ")[1]}: "
                              "Please check Prompts file")
        raise PromptError(f"\nUNVALID PROMPT: {err['input']}")

    print("\n\033[1;32m[OK] Input files parsed and validated.\033[0m\n")
    return (parser, validated_functions, validated_prompts)


if __name__ == "__main__":
    parser, functions, prompts = parse_and_check_args_and_files()
    print(parser)
    print(functions)
    print(prompts)
