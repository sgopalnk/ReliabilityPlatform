from pathlib import Path

def read_text_file(file_path: str) -> str:
    """
    Read and return the contents of a text file.
    """
    return Path(file_path).read_text(encoding="utf-8")

def write_text_file(file_path: str, content: str) -> None:
    """
    Write text content to a file.
    """
    path = Path(file_path)

    # Create parent directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(content, encoding="utf-8")
