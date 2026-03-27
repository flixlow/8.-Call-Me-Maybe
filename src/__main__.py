from src.parsing_validator import parse_and_check_args_and_files
from llm_sdk import Small_LLM_Model  # type: ignore
from src.obtain_functions import FunctionFinder
from src.obtain_args import ArgsFinder


def main() -> None:
    functions, prompts = parse_and_check_args_and_files()
    llm = Small_LLM_Model()

    function_finder = FunctionFinder(llm=llm, functions=functions)
    for prompt in prompts:
        func = function_finder.searching_function(prompt.prompt)
        if not func:
            print(f"prompt: {prompt.prompt} (function not found)")
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
