*This project has been created as part of the 42 curriculum by flauweri.*

# 8.-Call-Me-Maybe

## Description

## Instructions

## Resources
### AI Claude
- uv
- uv sync
- constrained decoding
- https://airbyte.com/data-engineering-resources/tokenization-vs-embeddings
- llm dimensions and coordonates
- BPE: découper le texte en morceaux intelligents (subwords)
- SentencePiece: bibliothèque de tokenization développée par Google.
- https://www.youtube.com/watch?v=4Bdc55j80l8
- https://docs.python.org/3/library/argparse.html
- https://docs.pydantic.dev/latest/
- https://stackoverflow.com/
- https://www.geeksforgeeks.org
- numpy.argmax()
- difference between tensors, ids and tokens
- https://www.aidancooper.co.uk/constrained-decoding/#what-is-constrained-decoding-and-how-does-it-work
- https://medium.com/@rosgluk/constraining-llms-with-structured-output-ollama-qwen3-python-or-go-2f56ff41d720




## Algorithm explanation
Describe your constrained decoding approach in detail

## Design decisions
Explain key choices in your implementation

## Performance analysis
Discuss accuracy, speed, and reliability of your solution

## Challenges faced
Document difficulties encountered and how you solved them
how to stop the prompt and implement the constrained decoding method ?
try:
- prompt argument only ?
- restraining with arg type set
- decoding to read if ther is a final double quotes
- constrained decoding on specified type
- 

## Testing strategy
Describe how you validated your implementation

## Example usage
Provide clear examples of running your program

[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 13, 1]

cd moulinette

uv run python -m moulinette prepare_exercises --set private

uv run python -m moulinette grade_student_answers --set private 

uv run python3 -m src --functions_definition moulinette/data/input/functions_definition.json --input moulinette/data/input/function_calling_tests.json --output data/output/function_calls.json

uv run python -m moulinette grade_student_answers --set private --student_answer_path ../data/output/function_calls.json

- Support for multiple LLM models beyond Qwen/Qwen3-0.6B : charlottemeyer/s1.1-20250515_160200
- Advanced error recovery mechanisms
- Demonstration of how encoding and decoding integrate with constrained decoding
- Vizualisation of the generation process
- 