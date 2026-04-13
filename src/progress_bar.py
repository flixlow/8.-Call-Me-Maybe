from typing import Generator


def i_gen(total: int) -> Generator[int]:
    """Generate a sequence of integers from 0 to total - 1.

    Args:
        total (int): Total number of iterations.

    Yields:
        int: The current iteration index.
    """
    for i in range(total):
        yield i


def print_progress_bar(progress: int, total: int, stage: str) -> None:
    """Display a progress bar in the terminal.

    Args:
        progress (int): Current progress value.
        total (int): Total number of steps.
        stage (str): Description of the current stage.
    """
    percent = 100 * (progress + 1) / total
    bar = '█' * int(percent) + '-' * (100 - int(percent))

    print(f"\rProgress: |{bar}| {percent:.1f}% {stage}", end="", flush=True)
