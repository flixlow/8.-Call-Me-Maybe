from src.parsing_validator import parse_and_check_args_and_files
from llm_sdk import Small_LLM_Model  # type: ignore
import numpy as np
from parsing_validator import Func


def is_function_in_working_prompt(prompt: str, functions: list[Func]) -> bool:
    for function in functions:
        if function.name in prompt:
            return True
    return False


def searching_function(llm: Small_LLM_Model,
                       functions: list[Func], prompt: str) -> str:
    """sorted logits to get function_name"""
    context = "answer a name of function :"

    functions_list = [function.name for function in functions]
    functions_name = str(functions_list.join(" "))

    working_prompt = context + functions_name + prompt

    while is_function_in_working_prompt(working_prompt, functions):
        ids = llm.encode()

        logits = llm.get_logits_from_input_ids(ids.tolist()[0])

        index_of_max_value = np.argmax(logits)

        result = llm.decode(index_of_max_value)

        working_prompt += result
    ret = working_prompt - prompt
    return ret


def main() -> None:
    functions, prompts = parse_and_check_args_and_files()
    llm = Small_LLM_Model()

    for prompt in prompts:
        current = prompt.prompt
        func = searching_function(llm, functions, current)
        print(f"{current}\n{func}")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)

# print("\033[1;32m[OK]\033[0m")
# print("\033[1;31m[ERROR]")
