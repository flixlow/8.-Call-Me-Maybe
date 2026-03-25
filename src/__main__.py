from src.parsing_validator import parse_and_check_args_and_files
from llm_sdk import Small_LLM_Model  # type: ignore
from src.obtain_functions import searching_function
from src.obtain_args import ArgsFinder


def main() -> None:
    functions, prompts = parse_and_check_args_and_files()
    llm = Small_LLM_Model()

    for prompt in prompts:
        func = searching_function(llm, functions, prompt.prompt)
        for function in functions:
            if function.name == func:
                arguments_finder = ArgsFinder(
                    llm=llm, function=function, prompt=prompt.prompt)
        print(f"{arguments_finder.searching_args()}")


if __name__ == '__main__':
    # try:
    main()
    # except Exception as e:
    # print(e)

# print("\033[1;32m[OK]\033[0m")
# print("\033[1;31m[ERROR]")
