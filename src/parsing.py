from argparse import ArgumentParser, Namespace


def parsing() -> Namespace:
    parser = ArgumentParser()

    flags = ["--functions_definition",
             "--input",
             "--output"]

    default_files = ["data/input/functions_definition.json",
                     "data/input/function_calling_tests.json",
                     "data/output/function_calls.json"]

    for flag, default_file in zip(flags, default_files):
        parser.add_argument(flag, default=default_file)

    return parser.parse_args()


if __name__ == "__main__":
    parser = parsing()
    print(parser.functions_definition)
    print(parser.input)
    print(parser.output)
