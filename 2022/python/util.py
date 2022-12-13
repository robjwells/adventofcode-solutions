from pathlib import Path


def read_input(day: int) -> str:
    input_file = Path("input", f"2022-{day:02}.txt")
    assert input_file.exists()
    return input_file.read_text()
