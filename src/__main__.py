from parsing import parsing
from input import open_json_file_to_list
from pydantic import BaseModel, RootModel, Field, field_validator


class Prompt(BaseModel):
    prompt: str

    @field_validator('prompt', mode='after')
    def is_prompt_empty(cls, prompt) -> str:
        if prompt == "" or prompt.isspace():
            raise ValueError("Empty prompt")
        return prompt


class CheckPromptFile(RootModel):
    root: list[Prompt]


class Func(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]


class CheckFunctionFile(RootModel):
    root: list[Func]


def main() -> None:
    parser = parsing()
    func = open_json_file_to_list(parser.functions_definition)
    prompt = open_json_file_to_list(parser.input)

    validated_func = CheckFunctionFile.model_validate(func)
    validated_prompt = CheckPromptFile.model_validate(prompt)
    prompt = [p.prompt for p in validated_prompt.root]
    print(prompt)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)

# print("\033[1;32m[OK]\033[0m")
# print("\033[1;31m[ERROR]")
