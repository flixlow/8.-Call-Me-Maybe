from llm_sdk import Small_LLM_Model
from parsing_validator import Func
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

    def parse_args(self, arg: str) -> dict:
        key_value = arg.split(':')
        arg_type = ""
        key = key_value[0].strip().strip('"')

        for k, v in self.function.parameters.items():
            if k == key:
                arg_type = v.type.value

        value = key_value[1].strip().strip('"')
        if arg_type == "number" or arg_type == "float":
            try:
                return {key: float(value)}
            except Exception:
                pass
        if arg_type == "integer":
            try:
                return {key: int(value)}
            except Exception:
                pass
        return {key: str(value)}

    def searching_args(self) -> dict:
        written = []
        context_ids = self.get_context()
        llm = self.llm

        args_input = self.encode_args_list()
        quotes_id = llm.encode('"').tolist()[0][0]
        index_of_max_value = quotes_id
        comma_id = llm.encode(', ').tolist()[0][0]
        ret: dict = {}

        for i in range(30):
            if index_of_max_value == quotes_id:
                if not args_input:
                    break
                arg = args_input.pop(0)
                context_ids.extend(arg)
                written.extend(arg)

            logits = llm.get_logits_from_input_ids(context_ids)
            index_of_max_value = int(np.argmax(logits))

            if '"' in llm.decode(index_of_max_value):
                index_of_max_value = quotes_id
                written.append(index_of_max_value)
                ret.update(self.parse_args(llm.decode(written)))
                if not args_input:
                    return ret
                else:
                    context_ids.append(index_of_max_value)
                    context_ids.append(comma_id)
                    written = []
                    continue

            written.append(index_of_max_value)
            context_ids.append(index_of_max_value)
        print("ERROR")
        return ret
