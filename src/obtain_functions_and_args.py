from llm_sdk import Small_LLM_Model  # type: ignore
import numpy as np


def get_prompt_for_function(functions: list, prompt: str) -> str:
    functions_list = [str(function.name) for function in functions]

    functions_name = "list of function name: " + " ".join(functions_list)

    return ("Choose the most relevant function for the request.\n"
            f"Available functions: {functions_name}\n"
            f"Request: {prompt}\n"
            "Answer a function name: ")


def searching_function(llm: Small_LLM_Model,
                       functions: list, prompt: str) -> str:

    context = get_prompt_for_function(functions, prompt)
    written = ""

    for i in range(50):
        ids = llm.encode(context)  # from str to tokens_ids

        logits = llm.get_logits_from_input_ids(ids.tolist()[0])
        # from ids_list to logits()
        index_of_max_value = [np.argmax(logits)]

        written += llm.decode(index_of_max_value)
        context += llm.decode(index_of_max_value)
        if any(function.name in written for function in functions):
            break

    for function in functions:
        if function.name in written:
            print(i)
            return function.name

    return "not found"
