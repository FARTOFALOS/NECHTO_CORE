from pathlib import Path


def save_text(path: str, content: str) -> None:
    Path(path).write_text(content)
