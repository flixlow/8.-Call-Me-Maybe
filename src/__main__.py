from llm_sdk import Small_LLM_Model  # type: ignore
from src.parse_and_validate import parse_and_check_args_and_files
from src.obtain_function_name import FunctionFinder
from src.obtain_args import ArgsFinder
from src.output import outputfile
from src.progress_bar import i_gen, print_progress_bar
from src.utils_classes import Prompt
from typing import Any


def main() -> None:
    """
    Main entry point for the script.

    Loads prompts and functions, finds the best function for each prompt,
    extracts arguments and writes results to a file.

    Returns:
        None
    """
    llm = Small_LLM_Model(model_name="Qwen/Qwen3-0.6B")
    # llm = Small_LLM_Model(model_name="charlottemeyer/s1.1-20250515_160200")

    parser, functions, prompts = parse_and_check_args_and_files()

    results: list[dict[str, Any]] = []

    function_finder = FunctionFinder(llm=llm, functions=functions)

    if parser.interactive is True:
        prompts = [Prompt(prompt=input("Please enter your prompt:"))]

    operations = len(prompts) * 3 + 1
    gen = i_gen(operations)

    for prompt in prompts:
        print_progress_bar(next(gen), operations, f"{'Searching Function':21}")
        func = function_finder.searching_function(prompt.prompt)
        if not func:
            results.append({"prompt": prompt.prompt,
                            "name": "(function not found)",
                            "parameters": "(parameter(s) not found)"})
            continue

        for function in functions:
            if function.name == func:
                arguments_finder = ArgsFinder(llm=llm, function=function,
                                              prompt=prompt.prompt)
        print_progress_bar(next(gen), operations, "Searching Argument(s)")
        args = arguments_finder.searching_args()
        if not args:
            args = {"argument(s)": "not found"}

        print_progress_bar(next(gen), operations, f"{'Formating results':21}")
        result = {"prompt": prompt.prompt,
                  "name": arguments_finder.function.name,
                  "parameters": args}
        results.append(result)

    print_progress_bar(next(gen), operations, f"{'Finish':21}")
    outputfile(parser, results)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n\033[1;31m[{type(e).__name__}]\033[0m\n{e}")
