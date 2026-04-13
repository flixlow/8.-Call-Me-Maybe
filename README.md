*This project has been created as part of the 42 curriculum by flauweri.*

# 8.-Call-Me-Maybe

## Description

Key concepts covered in this project include the understanding of LLMs (Large Language Models), tokenization, vectorization, argument schema validation, and the text generation process.

The project focuses on constrained decoding, a technique that restricts the model’s output to only valid function names and argument types at each step. This ensures that generated outputs are always structured and machine-executable.

The main goal is to reliably extract arguments from user requests that match a predefined schema, providing both robustness and reliability for function calling with LLMs.

## Instructions

### Installation
Install all dependencies:
```sh
make install
```

### Running the Project
Run the main program with default input and output files:
```sh
make run
```

### Debug Mode
Run with the Python debugger:
```sh
make debug
```

### Linting & Type Checking
Check code style and types:
```sh
make lint
```
Strict linting and type checking:
```sh
make lint-strict
```

### Cleaning
Remove cache, .venv and output files:
```sh
make clean
```

### Custom Input/Output Paths
To use custom input or output files:
```sh
uv run python -m src [--functions_definition <function_definition_file>] [--input <input_file>] [--output <output_file>]
```

## Resources

### Documentation & Tutorials
- [Tokenization vs Embeddings (Airbyte)](https://airbyte.com/data-engineering-resources/tokenization-vs-embeddings)
- [What is constrained decoding? (Aidan Cooper)](https://www.aidancooper.co.uk/constrained-decoding/#what-is-constrained-decoding-and-how-does-it-work)
- [Constraining LLMs with structured output (Medium)](https://medium.com/@rosgluk/constraining-llms-with-structured-output-ollama-qwen3-python-or-go-2f56ff41d720)
- [YouTube: Progress bar](https://www.youtube.com/watch?v=oJLaA7-i3nI)
- [YouTube: Tokenization and LLMs](https://www.youtube.com/watch?v=4Bdc55j80l8)
- [Python argparse documentation](https://docs.python.org/3/library/argparse.html)
- [Pydantic documentation](https://docs.pydantic.dev/latest/)
- [Stack Overflow](https://stackoverflow.com/)
- [GeeksforGeeks](https://www.geeksforgeeks.org)

### Key Concepts & Definitions
- **uv**: Python package/dependency manager.
- **Embedding dimension**: Size of the vector representing a token in the model.
- **Model parameters**: Numeric values (weights) learned during training, stored in matrices.
- **Qwen3-0.6B**: LLM with 0.6 billion parameters.
- **Logits**: Raw model scores before applying softmax to get probabilities.
- **BPE (Byte Pair Encoding)**: Subword tokenization algorithm.
- **SentencePiece**: Google library for unsupervised text tokenization.
- **numpy.argmax()**: Returns the index of the max value in a NumPy array.
- **Regex**: Pattern for searching or validating text.
- **ASCII/Unicode/UTF-8**: Character encodings.
- **Tensors, ids, tokens**: Tensors are multi-dimensional arrays; ids are token indices; tokens are text units.
- **Attention**: Mechanism in LLMs to focus on relevant input parts.
- **Temperature**: Controls randomness in model output.

### AI Used in This Project
- Improved error messages
- README and docstring assistance


## Algorithm explanation

The algorithm applies constrained decoding in two main steps: function name selection and argument extraction.

1. All possible function names are tokenized and stored as lists of token IDs.
2. The context is also tokenized into token IDs.
3. For each decoding step, the model computes logits (probabilities) for the next possible tokens using get_logits_from_next_ids().
4. Only tokens that can continue a valid function name are considered. The token with the highest probability is added to the output.
5. When a complete function name is found, it is returned.
6. For argument extraction, the context is encoded one argument at a time using the format: "{argument_name}"=". When a double quote is found in the generated output, the next argument is added to the context and the process repeats for each argument in sequence. It returns when there is no more argument.
7. For arguments:
	- If the argument is a number (int or float), only numeric tokens ('0123456789".') are allowed.
	- For other types, the token with the highest logit is selected.

This process ensures that only valid function names and argument types are generated, following the predefined schema.

#### context for function name selection

```
Choose the most relevant function for the request.
list of function name: fn_add_number|fn_greet|...|fn_substitute_string_with_regex
Request: {prompt}
Answer a function name:
```

#### context for arguments extraction

```
Extract intact argument from request
Function name=fn_add_numbers
Request=What is the sum of 2 and 3?
Argument=
argument_name=a type=number
argument_name=b type=number
```

then add:
```
"a"= "
```

waiting for double quotes, then add:
```
"b"= "
```

## Design decisions
Input arguments are validated using the argparse module.
The codebase is modular and object-oriented, using Pydantic's BaseModel for robust data validation and clear structure. Function and argument extraction are handled by separate classes (`FunctionFinder` and `ArgsFinder`), making the logic easy to extend and maintain. Custom error classes provide clear feedback for file, argument, and validation issues. Utility modules (e.g., for progress bars and prompt validation) keep the main logic clean and focused.


## Performance analysis
The solution is accurate for well-formed prompts and function definitions, as it uses constrained decoding and schema validation to minimize errors. Speed is suitable for small to medium datasets, with progress bars for user feedback. Reliability is enhanced by robust error handling and clear separation of concerns, but performance may depend on the underlying LLM and input size.

For function name search, the algorithm is optimized to minimize the number of encode/decode operations, improving efficiency. For argument extraction, this optimization is not possible because the double quote token (used to delimit arguments) can appear in many different token forms, requiring more flexible decoding.

## Challenges faced
Key challenges included:
- Designing a decoding loop that stops at the right moment for both function names and arguments.
- Restricting generation to valid argument types (e.g., only digits for numbers).

Solutions:
- Used argument-by-argument context encoding and checked for closing quotes to delimit arguments.
- Implemented type-based token restrictions and fallback logic for missing arguments.
- Added custom error classes for clear user feedback.

## Testing strategy
Testing began with interactive input mode to understand token generation, using a simple encode/decode and print loop. Once prompt and function parsing were implemented, the system was tested with the prompts provided in the subject. Additional validation was performed using manual prompt testing to ensure correctness and robustness.

## Example usage
Example input prompt in JSON:
```json
{
    "prompt": "Replace all vowels in 'Programming is fun' with asterisks"
}
```

Example function definition:
```json
{
    "name": "fn_substitute_string_with_regex",
    "description": "Replace all occurrences matching a regex pattern in a string.",
    "parameters": {
      "source_string": { "type": "string" },
      "regex": { "type": "string" },
      "replacement": { "type": "string" }
    },
    "returns": { "type": "string" }
}
```

Example result:
```json
{
    "prompt": "Replace all vowels in 'Programming is fun' with asterisks",
    "name": "fn_substitute_string_with_regex",
    "parameters": {
        "source_string": "Programming is fun",
        "regex": "([aeiouAEIOU])",
        "replacement": "*"
    }
}
```

## Bonus

- Progress bar to visualize generating process
- 'interactive' mode pour prompt entry
- Advanced error recovery system
- Support multiple LLMs
- Demonstration of how encoding and decoding work with constrained decoding