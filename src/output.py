from argparse import Namespace
from pathlib import Path
from typing import Any
import json
import os


def outputfile(parser: Namespace, results: list[dict[str, Any]]) -> None:
    """Write results to an output file in JSON format.

    Args:
        parser (Namespace): The argparse object containing the output path.
        results (list[dict[str, Any]]): The results to write to the file.
    """
    output = Path(parser.output)
    try:
        os.mkdir(output.parent)
    except FileExistsError:
        pass
    with open(str(output), 'w') as f:
        json.dump(results, f, indent=4)
    print(f"\n\n\033[1;32m[OK] Output file done: {str(output)}\033[0m")
