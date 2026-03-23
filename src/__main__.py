from src.parsing_validator import parse_and_check_args_and_files
from llm_sdk import Small_LLM_Model  # type: ignore
import numpy as np


def searching_function(llm: Small_LLM_Model,
                       functions: list, prompt: str) -> str:
    """sorted logits to get function_name"""
    functions_list = [str(function.name) for function in functions]
    functions_name = "list of function name: " + " ".join(functions_list)

    context = (f"answer a name of function :\n{functions_name}"
               f"\n{prompt}\nfunction name: ")

    written = ""
    i = 0

    while i < 50:
        ids = llm.encode(context)

        logits = llm.get_logits_from_input_ids(ids.tolist()[0])

        index_of_max_value = np.argmax(logits)

        written += llm.decode(index_of_max_value)
        context += llm.decode(index_of_max_value)
        if any(function.name in written for function in functions):
            break
        i += 1

    for function in functions:
        if function.name in written:
            print(i)
            return function.name

    return "not found"


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
