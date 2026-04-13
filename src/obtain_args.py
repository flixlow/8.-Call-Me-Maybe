from llm_sdk import Small_LLM_Model  # type: ignore
from src.utils_classes import Func
from pydantic import BaseModel, ConfigDict, PrivateAttr
import numpy as np
from typing import Any


class ArgsFinder(BaseModel):
    """
    Extracts function arguments from a user request.

    Attributes:
        llm (Small_LLM_Model): Language model used for encoding and generation.
        function (Func): Target function for which to extract arguments.
        prompt (str): User request to analyze.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    llm: Small_LLM_Model
    function: Func
    prompt: str
    _context_ids: list[int] = PrivateAttr()
    _args_input: list[list[int]] = PrivateAttr()
    _args_type: list[str] = PrivateAttr()
    _numbers: list[int] = PrivateAttr()

    def model_post_init(self, _: Any) -> None:
        self._context_ids = self.get_context()
        self._args_input = self.encode_args_list()
        self._args_type = [arg.type.value
                           for arg in self.function.parameters.values()]
        self._numbers = [self.llm.encode(n).tolist()[0][0]
                         for n in list('0123456789.-"')]

    def get_context(self) -> list[int]:
        """
        Build the encoding context for argument extraction.

        Returns:
            list[int]: Encoded context IDs for the LLM.
        """
        func = self.function
        arg_context = ""
        for k, v in func.parameters.items():
            arg_context += f"\nargument_name={k} type={v.type.value}"
        context = ("Extract intact argument from request"
                   f"\nFunction name={func.name}"
                   f"\nRequest={self.prompt}"
                   f"\nArgument={arg_context}")

        context_ids: list[int] = self.llm.encode(context).tolist()[0]
        return context_ids

    def encode_args_list(self) -> list[list[int]]:
        """
        Encode each function argument as a list of token IDs.

        Returns:
            list[list[int]]: List of encoded token IDs for each argument.
        """
        args_line = [f'{k}= "' for k in self.function.parameters.keys()]
        return [self.llm.encode(arg).tolist()[0] for arg in args_line]

    def parse_args(self, arg: str) -> dict[str, Any]:
        """
        Parse an encoded argument string and convert it to the correct type.

        Args:
            arg (str): Argument as a string (e.g., 'x= 42').

        Returns:
            dict: Dictionary {argument_name: typed_value}.
        """
        key_value = arg.split('=')
        arg_type = ""
        key = key_value[0].strip().strip('"')
        for k, v in self.function.parameters.items():
            if k == key:
                arg_type = v.type.value
        value = key_value[1].strip()
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

    def get_number(self, logits: list[float]) -> int:
        constrained = {}
        for n in self._numbers:
            constrained.update({n: logits[n]})

        return max(constrained, key=lambda x: constrained[x])

    def searching_args(self) -> dict[str, Any] | None:
        """
        Search and extract arguments from the user request using the LLM.

        Returns:
            dict: Dictionary of extracted arguments with their typed values.
        """
        written = []
        llm = self.llm
        quotes_id = llm.encode('"').tolist()[0][0]
        index_of_max_value = quotes_id
        ret: dict[str, Any] = {}

        for _ in range(35):
            if index_of_max_value == quotes_id:
                if not self._args_input or not self._args_type:
                    break
                arg = self._args_input.pop(0)
                arg_type = self._args_type.pop(0)
                self._context_ids.extend(arg)
                written.extend(arg)

            logits = llm.get_logits_from_input_ids(self._context_ids)
            if arg_type in ["float", "integer", "number"]:
                index_of_max_value = self.get_number(logits)
            else:
                index_of_max_value = int(np.argmax(logits))

            if '"' in llm.decode(index_of_max_value):
                written.append(index_of_max_value)
                ret.update(self.parse_args(
                        llm.decode(written).replace("\"", "")))
                index_of_max_value = quotes_id
                if not self._args_input:
                    return ret
                else:
                    self._context_ids.append(index_of_max_value)
                    written = []
                    continue

            written.append(index_of_max_value)
            self._context_ids.append(index_of_max_value)
        return None
