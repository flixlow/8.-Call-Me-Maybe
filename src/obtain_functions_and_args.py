from llm_sdk import Small_LLM_Model  # type: ignore
import numpy as np


def get_prompt_for_function(functions: list, prompt: str) -> str:
    functions_list = [str(function.name) for function in functions]

    functions_name = "list of function name: " + "|".join(functions_list)

    return ("Choose the most relevant function for the request.\n"
            f"Available functions: {functions_name}\n"
            f"Request: {prompt}\n"
            "Answer a function name: ")


def get_tab_ids_of_functions_name(llm: Small_LLM_Model,
                                  functions: list) -> list[list[int]]:
    tab = []
    for function in functions:
        tab.append(llm.encode(function.name).tolist()[0])
    return tab


def get_available_tokens(tab: list[list[int]],
                         written: list[int]) -> list[int]:
    available_tokens = []
    for function in tab:
        if (function[:len(written)] == written):
            available_tokens.append(function[len(written)])
    return available_tokens


def searching_function(llm: Small_LLM_Model,
                       functions: list, prompt: str) -> str:

    context = get_prompt_for_function(functions, prompt)
    tab = get_tab_ids_of_functions_name(llm, functions)
    written: list = []

    for i in range(30):
        ids = llm.encode(context)

        functions_tokens = get_available_tokens(tab, written)

        logits = llm.get_logits_from_input_ids(ids.tolist()[0])

        index_of_max_value = [np.argmax(logits)]

        written += llm.decode(index_of_max_value)
        context += llm.decode(index_of_max_value)

        for function in functions:
            if function.name in written:
                print(i)
                return function.name

    return "not found"
