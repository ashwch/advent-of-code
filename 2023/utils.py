from pathlib import Path

def get_input(day: int, iterator: bool = False) -> str:
    """Return the input for the given day."""
    file_obj = (Path(__file__).parent / f"inputs/day_{day}.txt")
    if iterator:
        return file_obj.open()
    else:
        return file_obj.read_text()
