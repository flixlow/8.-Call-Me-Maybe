from typing import Generator


def i_gen(total: int) -> Generator[int]:
    for i in range(total):
        yield i


def print_progress_bar(progress: int, total: int, stage: str) -> None:
    percent = 100 * (progress + 1) / total
    bar = '█' * int(percent) + '-' * (100 - int(percent))

    print(f"\rProgress: |{bar}| {percent:.1f}% {stage}", end="", flush=True)
