import argparse


def parsing() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    for arg in ["functions_definition", "input", "output"]:
        parser.add_argument(f"--{arg}", default="data/input/functions_definition.json")

    try:
        result = parser.parse_args()
    except FileNotFoundError as e:
        print(e)

    return result


if __name__ == "__main__":
    parser = parsing()
    print(parser.functions_definition)
    print(parser.input)
    print(parser.output)
