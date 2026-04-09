from llm_sdk import Small_LLM_Model
from src.parsing_validator import Func
from pydantic import BaseModel, ConfigDict


class FunctionFinder(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    llm: Small_LLM_Model
    functions: list[Func]

    def get_context(self, prompt: str) -> list[int]:
        functions_list = [str(function.name) for function in self.functions]
        functions_name = "list of function name: " + "|".join(functions_list)
        context = ("Choose the most relevant function for the request.\n"
                   f"{functions_name}\n"
                   f"Request: {prompt}\n"
                   "Answer a function name: ")
        return self.llm.encode(context).tolist()[0]

    def get_tab_ids_of_functions_name(self) -> list[list[int]]:
        tab = []
        for function in self.functions:
            tab.append(self.llm.encode(function.name).tolist()[0])
        return tab

    def get_available_tokens(self, tab: list[list[int]],
                             written: list[int]) -> set[int]:
        available_tokens = set()
        for function in tab:
            if function[:len(written)] == written:
                available_tokens.add(function[len(written)])
        return available_tokens

    def searching_function(self, prompt: str) -> str | None:
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
