from llm_sdk import Small_LLM_Model  # type: ignore
from src.parse_and_validate import parse_and_check_args_and_files
from src.obtain_function_name import FunctionFinder
from src.obtain_args import ArgsFinder
from pathlib import Path
from typing import Any
import json
import os


def main() -> None:
    """
    Main entry point for the script. Loads prompts and functions,
    finds the best function for each prompt, extracts arguments,
    and writes results to a file.

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
            results.append({"prompt": prompt.prompt,
                            "name": "(function not found)",
                            "parameters": "(parameter(s) not found)"})
            continue

        for function in functions:
            if function.name == func:
                arguments_finder = ArgsFinder(
                    llm=llm, function=function, prompt=prompt.prompt)

        args = arguments_finder.searching_args()

        if not args:
            args = {"argument(s)": "not found"}

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
        print(f"\n\033[1;31m[{type(e).__name__}]\033[0m\n{e}")
    else:
        print("\033[1;32m[OK]\033[0m")
