class FileOpeningError(Exception):
    pass


class FunctionError(Exception):
    pass


class PromptError(Exception):
    pass


class ArgumentError(Exception):
    def __init__(self, message: str = (
            "\nInvalid command-line arguments."
            "\nPlease ensure all required arguments are provided:"
            "\n[--functions_definition FUNCTIONS_DEFINITION]"
            "\n[--input INPUT]"
            "\n[--output OUTPUT]")) -> None:
        super().__init__(message)
