from llm_sdk import Small_LLM_Model  # type: ignore
from src.parsing_validator import parse_and_check_args_and_files
from src.obtain_functions import FunctionFinder
from src.obtain_args import ArgsFinder
from pathlib import Path
from typing import Any
import json
import os


def main() -> None:
    """
    Main entry point for the script. Loads prompts and functions,
    finds the best function for each prompt,
    extracts arguments, and writes results to a file.

    Returns:
        None
    """
    parser, functions, prompts = parse_and_check_args_and_files()

    llm = Small_LLM_Model(model_name="Qwen/Qwen3-0.6B")
    results: list[dict[str, Any]] = []

    function_finder = FunctionFinder(llm=llm, functions=functions)
    for prompt in prompts:
        func = function_finder.searching_function(prompt.prompt)
        if not func:
            print(f"prompt: {prompt.prompt} (function not found)")

        for function in functions:
            if function.name == func:
                arguments_finder = ArgsFinder(
                    llm=llm, function=function, prompt=prompt.prompt)
        args = arguments_finder.searching_args()
        result = {"prompt": prompt.prompt,
                  "name": arguments_finder.function.name,
                  "parameters": args}
        results.append(result)

    output = Path(parser.output)
    try:
        os.mkdir(output.parent)
    except FileExistsError:
        pass
    with open(str(output), 'w') as f:
        json.dump(results, f, indent=4)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\033[1;31m[ERROR]{e}")
    else:
        print("\033[1;32m[OK]\033[0m")
