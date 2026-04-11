UV_RUN = uv run python3 -m

install:
	uv sync
	@echo "\033[0;32m\n[OK] installation completed ✔\n\033[0m"

run:
	$(UV_RUN) src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calling_results.json

debug: install
	$(UV_RUN)  pdb -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calling_results.json

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf data/output
	rm -rf .venv

lint:
	flake8 src && mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(UV_RUN) flake8 src && $(UV_RUN) mypy src --strict

.PHONY: install run debug clean fclean lint lint-strict