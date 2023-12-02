from pathlib import Path

def get_input(day: int) -> str:
    """Return the input for the given day."""
    return (Path(__file__).parent / f"inputs/day_{day}.txt").read_text()
