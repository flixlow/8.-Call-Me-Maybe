from pydantic import BaseModel, TypeAdapter
from pydantic import Field, field_validator
from argparse import ArgumentParser, Namespace
from enum import Enum
import json


class ArgType(Enum):
    NUMBER = "number"
    STRING = "string"
    FLOAT = "float"
    INTEGER = "integer"
    BOOLEAN = "boolean"


class Type(BaseModel):
    type: ArgType


class Func(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: dict[str, Type]
    returns: dict[str, str]


class Prompt(BaseModel):
    prompt: str

    @field_validator('prompt', mode='after')
    def is_prompt_empty(cls, prompt: str) -> str:
        if prompt == "" or prompt.isspace():
            raise ValueError("Empty prompt")
        return prompt


def open_json_file_to_list(file_name: str) -> list:
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data


def parsing() -> Namespace:
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


def parse_and_check_args_and_files() -> tuple[
        Namespace, list[Func], list[Prompt]]:
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
