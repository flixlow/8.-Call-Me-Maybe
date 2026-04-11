from argparse import Namespace
from pathlib import Path
from typing import Any
import json
import os


def outputfile(parser: Namespace, results: list[dict[str, Any]]) -> None:
    output = Path(parser.output)
    try:
        os.mkdir(output.parent)
    except FileExistsError:
        pass
    with open(str(output), 'w') as f:
        json.dump(results, f, indent=4)
