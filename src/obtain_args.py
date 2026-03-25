from llm_sdk import Small_LLM_Model  # type: ignore
from src.parsing_validator import Func
import numpy as np


def get_context(function: str, parameters: dict, prompt: str) -> str:
    text = ""

    for k, v in parameters.items():
        text += f"argument_name = {k}, type = ({v.type.name})\n"

    return ("Answer only with the appropriate argument of Request:"
            f"\nFunction name: {function}"
            f"\nRequest: {prompt}"
            f"\nArgument(s):\n{text}")


def searching_args(llm: Small_LLM_Model,
                   function: Func, prompt: str) -> dict[str, str | dict]:
    context = get_context(function.name, function.parameters, prompt)

    written = []
    args_lign = [f"{k}: '" for k in function.parameters.keys()]
    text = [llm.encode(arg).tolist()[0] for arg in args_lign]
    ids: list = llm.encode(context).tolist()[0]
    id_double_quotes = llm.encode("'").tolist()[0]
    index_of_max_value = id_double_quotes

    for i in range(12):
        if text == []:
            break

        if index_of_max_value == id_double_quotes:
            arg = text.pop(0)
            ids.extend(arg)
            written.extend(arg)

        logits = llm.get_logits_from_input_ids(ids)
        index_of_max_value = int(np.argmax(logits))
        written.append(index_of_max_value)
        ids.append(index_of_max_value)
        i += 1

    print("".join(llm.decode(written)))

    return {
        "prompt": prompt,
        "name": function.name,
        "parameters": "None"
    }
