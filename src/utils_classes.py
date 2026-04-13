from pydantic import BaseModel, Field, field_validator
from enum import Enum


class ArgType(Enum):
    """
    Enumeration of possible argument types for a function.
    """
    NUMBER = "number"
    STRING = "string"
    FLOAT = "float"
    INTEGER = "integer"
    BOOLEAN = "boolean"


class Type(BaseModel):
    """Represents the type of a function argument.

    Attributes:
        type (ArgType): The argument type.
    """
    type: ArgType


class Func(BaseModel):
    """Represents a function to be called.

    Attributes:
        name (str): Name of the function.
        description (str): Description of the function.
        parameters (dict[str, Type]): Function parameters.
        returns (dict[str, str]): Function return types.
    """
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: dict[str, Type]
    returns: dict[str, str]


class Prompt(BaseModel):
    """Represents a user prompt.

    Attributes:
        prompt (str): The user prompt text.
    """
    prompt: str

    @field_validator('prompt', mode='after')
    def is_prompt_empty(cls, prompt: str) -> str:
        """Validate that the prompt is not empty or only whitespace.

        Args:
            prompt (str): The user prompt text.

        Returns:
            str: The validated prompt.

        Raises:
            ValueError: If the prompt is empty or only whitespace.
        """
        if prompt == "" or prompt.isspace():
            raise ValueError("Empty prompt")
        return prompt
