from llm_sdk import Small_LLM_Model  # type: ignore


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
                         written: list[int]) -> set[int]:
    available_tokens = set()
    for function in tab:
        if function[:len(written)] == written:
            available_tokens.add(function[len(written)])
    return available_tokens


def searching_function(llm: Small_LLM_Model,
                       functions: list, prompt: str) -> str:
    context = get_prompt_for_function(functions, prompt)
    tab = get_tab_ids_of_functions_name(llm, functions)

    written: list = []
    ids: list = llm.encode(context).tolist()[0]

    for i in range(10):
        available_tokens = get_available_tokens(tab, written)

        logits = llm.get_logits_from_input_ids(ids)

        constrained = {}
        for tokens in available_tokens:
            constrained.update({tokens: logits[tokens]})

        highest_probability = max(constrained, key=lambda x: constrained[x])

        written.append(highest_probability)
        ids.append(highest_probability)

        for function_token_tab in tab:
            if function_token_tab == written:
                return llm.decode(written)

    return "not found"
