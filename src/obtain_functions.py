from llm_sdk import Small_LLM_Model  # type: ignore
from src.utils_class import Func
from pydantic import BaseModel, ConfigDict


class FunctionFinder(BaseModel):
    """
    Finds the most relevant function for a user request.

    Attributes:
        llm (Small_LLM_Model): Language model used for encoding and generation.
        functions (list[Func]): List of candidate functions.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    llm: Small_LLM_Model
    functions: list[Func]

    def get_context(self, prompt: str) -> list[int]:
        """
        Build the encoding context for function selection.

        Args:
            prompt (str): The user request.

        Returns:
            list[int]: Encoded context IDs for the LLM.
        """
        functions_list = [str(function.name) for function in self.functions]
        functions_name = "list of function name: " + "|".join(functions_list)
        context = ("Choose the most relevant function for the request.\n"
                   f"{functions_name}\n"
                   f"Request: {prompt}\n"
                   "Answer a function name: ")
        return self.llm.encode(context).tolist()[0]

    def get_tab_ids_of_functions_name(self) -> list[list[int]]:
        """
        Encode all function names as lists of token IDs.

        Returns:
            list[list[int]]: List of encoded token IDs for each function name.
        """
        tab = []
        for function in self.functions:
            tab.append(self.llm.encode(function.name).tolist()[0])
        return tab

    def get_available_tokens(self, tab: list[list[int]],
                             written: list[int]) -> set[int]:
        """
        Return available tokens for completing a function name.

        Args:
            tab (list[list[int]]): List of encoded function name token IDs.
            written (list[int]): Already generated token IDs.

        Returns:
            set[int]: Valid tokens for completion.
        """
        available_tokens = set()
        for function in tab:
            if function[:len(written)] == written:
                available_tokens.add(function[len(written)])
        return available_tokens

    def searching_function(self, prompt: str) -> str | None:
        """
        Search for the most relevant function for the user request.

        Args:
            prompt (str): The user request.

        Returns:
            str | None: The found function name, or None if not found.
        """
        llm = self.llm
        generated: list = []
        ids = self.get_context(prompt)
        tok_functions = self.get_tab_ids_of_functions_name()

        for _ in range(12):
            constrained = {}
            logits = llm.get_logits_from_input_ids(ids)

            for tokens in self.get_available_tokens(tok_functions, generated):
                constrained.update({tokens: logits[tokens]})

            highest_probability_token = max(
                constrained, key=lambda x: constrained[x])

            generated.append(highest_probability_token)
            ids.append(highest_probability_token)

            for function in tok_functions:
                if function == generated:
                    return llm.decode(generated)

        return None
