from pathlib import Path
from typing import Dict, List

POETRY_VERSIONS: Dict[str, List[int]] = {"1.1": [14]}
PYTHON_VERSIONS: Dict[str, List[int]] = {"3.10": [6]}
PYTHON_VARIATIONS: List[str] = ["bullseye", "slim-bullseye"]

PROJECT_ROOT: Path = Path(__file__).resolve().parent

def get_dockerfile_version(
    minor_version: str,
    versions: Dict[str, List[int]],
) -> str:
    return f"{minor_version}.{max(versions[minor_version])}"
