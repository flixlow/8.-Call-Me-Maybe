$(DEP) = 

install:
python3 -m uv venv .venv
python3 -m uv venv activate .venv

run:
uv run python -m src [--functions_definition <function_definition_file>] [--input <input_file>] [--
output <output_file>]

debug:

clean:

lint:
flake8 . && mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
flake8 . && mypy . -- strict