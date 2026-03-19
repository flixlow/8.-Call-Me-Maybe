MAIN_PROGRAM = src
VENV = .venv
V_PYTHON = $(VENV)/bin/python3
V_PIP = $(V_PYTHON) -m pip
V_UV = $(VENV)/bin/uv
LLM = llm_sdk

install: $(VENV)
	$(V_PIP) install uv
	$(V_UV) sync --project $(LLM) --cache-dir /tmp/uv_cache
	$(V_UV) build --project $(LLM) --cache-dir /tmp/uv_cache
	$(V_UV) sync
	@echo "\033[1;32m\n[OK] installation completed ✔\n"

$(VENV):
	python3 -m venv $(VENV)

run:
	uv run python -m $(MAIN_PROGRAM) --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calls.json

debug: install
	$(PYTHON) -m pdb $(MAIN_PROGRAM)

clean:

lint:
	flake8 . && mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 . && mypy . -- strict