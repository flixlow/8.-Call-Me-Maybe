class FileOpeningError(Exception):
    """Exception raised when a JSON file cannot be opened or parsed."""
    pass


class FunctionError(Exception):
    """Exception raised when there are issues with function validation."""
    pass


class PromptError(Exception):
    """Exception raised when there are issues with prompt validation."""
    pass


class ArgumentError(Exception):
    """Exception raised for invalid command-line arguments."""

    def __init__(self, message: str = (
            "\nInvalid command-line arguments."
            "\nPlease ensure all required arguments are provided:"
            "\n[--functions_definition FUNCTIONS_DEFINITION]"
            "\n[--input INPUT]"
            "\n[--output OUTPUT]")) -> None:
        """Initialize the ArgumentError with a custom message.

        Args:
            message (str): Error message describing the invalid arguments.
        """
        super().__init__(message)
