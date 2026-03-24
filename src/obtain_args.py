from llm_sdk import Small_LLM_Model  # type: ignore
from src.parsing_validator import Func


def searching_args(llm: Small_LLM_Model,
                   function: Func, prompt: str) -> dict[str, str | dict]:

    return {
        "prompt": prompt,
        "name": function.name,
        "parameters": {"a": 2.0, "b": 3.0}
    }
