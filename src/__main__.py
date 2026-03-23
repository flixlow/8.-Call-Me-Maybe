from src.parsing_validator import parse_and_check_args_and_files
from llm_sdk import Small_LLM_Model


def main() -> None:
    functions, prompts = parse_and_check_args_and_files()
    llm = Small_LLM_Model()
    id = llm.encode(prompts[0])
    print(llm.get_logits_from_input_ids(id))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)

# print("\033[1;32m[OK]\033[0m")
# print("\033[1;31m[ERROR]")
