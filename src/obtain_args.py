from llm_sdk import Small_LLM_Model  # type: ignore
from src.parsing_validator import Func, ArgType
from pydantic import BaseModel, ConfigDict
import numpy as np


class ArgsFinder(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    llm: Small_LLM_Model
    function: Func
    prompt: str

    def get_context(self) -> list[int]:
        func = self.function
        arg_context = ""

        for k, v in func.parameters.items():
            arg_context += f"\nargument_name: {k}, type: {v.type.value}"

        context = ("Answer only with the appropriate argument of Request:"
                   f"\nFunction name: {func.name}"
                   f"\nRequest: {self.prompt}"
                   f"\nArgument(s):{arg_context}")

        return self.llm.encode(context).tolist()[0]

    def encode_args_list(self) -> list[list[int]]:
        """return a tab[str] on every argument to input in context"""
        args_lign = [f'{k}: "' for k in self.function.parameters.keys()]

        return [self.llm.encode(arg).tolist()[0] for arg in args_lign]

    def get_id_set(self) -> list[int]:
        for parameter in self.function.parameters.values():
            print(parameter.type.name)
        return []

    def searching_args(self) -> str:
        written = []
        ids = self.get_context()
        llm = self.llm

        args_input = self.encode_args_list()
        quotes_id = llm.encode('"').tolist()[0][0]
        index_of_max_value = quotes_id
        comma_id = llm.encode(', ').tolist()[0][0]

        for i in range(30):
            if index_of_max_value == quotes_id:
                if not args_input:
                    break
                arg = args_input.pop(0)
                ids.extend(arg)
                written.extend(arg)

            logits = llm.get_logits_from_input_ids(ids)
            index_of_max_value = int(np.argmax(logits))  # we must implement a constrained decoding here with only given set of char

            if '"' in llm.decode(index_of_max_value):
                index_of_max_value = quotes_id
                if not args_input:
                    written.append(index_of_max_value)
                    return llm.decode(written)
                else:
                    written.append(index_of_max_value)
                    written.append(comma_id)
                    ids.append(index_of_max_value)
                    ids.append(comma_id)
                    continue
            written.append(index_of_max_value)
            ids.append(index_of_max_value)

        return self.llm.decode(written)

# NUMBER = "number" + '"'
# STRING = "string" + '"'
# FLOAT = "float" + '"'
# INTEGER = "integer" + '"'
# BOOLEAN = "boolean" + '"'
