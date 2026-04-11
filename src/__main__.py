from llm_sdk import Small_LLM_Model  # type: ignore
from src.parse_and_validate import parse_and_check_args_and_files
from src.obtain_function_name import FunctionFinder
from src.obtain_args import ArgsFinder
from src.output import outputfile
from typing import Any, Generator


def i_gen(total: int) -> Generator[int]:
    for i in range(total):
        yield i


def print_progress_bar(progress: int, total: int, stage: str) -> None:
    percent = 100 * (progress + 1) / total
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    # if percent == 100:
    #     print(f"\rProgress: 100.0% {' ' * 124}", flush=True)
    #     return
    print(f"\rProgress: |{bar}| {percent:.1f}% {stage}", end="", flush=True)


def main() -> None:
    """
    Main entry point for the script.

    Loads prompts and functions, finds the best function for each prompt,
    extracts arguments and writes results to a file.

    Returns:
        None
    """
    llm = Small_LLM_Model(model_name="Qwen/Qwen3-0.6B")

    parser, functions, prompts = parse_and_check_args_and_files()

    results: list[dict[str, Any]] = []
    function_finder = FunctionFinder(llm=llm, functions=functions)
    operations = len(prompts) * 3 + 1
    gen = i_gen(operations)

    for i, prompt in enumerate(prompts):
        print_progress_bar(next(gen), operations, f"{'Searching Function':21}")
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
