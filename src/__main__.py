from src.parsing_validator import parse_and_check_args_and_files
from llm_sdk import Small_LLM_Model  # type: ignore
from src.obtain_functions import searching_function
from src.obtain_args import searching_args


def main() -> None:
    functions, prompts = parse_and_check_args_and_files()
    llm = Small_LLM_Model()

    print(functions)

    for prompt in prompts:
        current = prompt.prompt
        func = searching_function(llm, functions, current)
        for function in functions:
            if function.name == func:
                output = searching_args(llm, function, current)
        print(f"{output}")


if __name__ == '__main__':
    # try:
    main()
    # except Exception as e:
    # print(e)

# print("\033[1;32m[OK]\033[0m")
# print("\033[1;31m[ERROR]")
