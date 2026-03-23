from src.parsing_validator import parse_and_check_args_and_files
from llm_sdk import Small_LLM_Model  # type: ignore
from src.obtain_functions_and_args import searching_function


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
