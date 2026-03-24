from llm_sdk import Small_LLM_Model  # type: ignore
from src.parsing_validator import Func


def get_context(function: str, parameters: dict, prompt: str) -> str:
    return (f"function name: {function}"
            f"Request: {prompt}"
            f"replace Type() by the appropriate argument of request: {parameters}")


def searching_args(llm: Small_LLM_Model,
                   function: Func, prompt: str) -> dict[str, str | dict]:
    context = get_context(function.name, function.parameters, prompt)
    i = 0
    written = []

    while i < 12:
        

    return {
        "prompt": prompt,
        "name": function.name,
        "parameters": function.parameters
    }
