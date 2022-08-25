from pathlib import Path
from typing import Dict, List

POETRY_VERSIONS: Dict[str, List[int]] = {"1.1": [14]}
PYTHON_VERSIONS: Dict[str, List[int]] = {"3.10": [6]}
PYTHON_VARIATIONS: Dict[str, List[str]] = {
    "bullseye": ["", "-bullseye"],
    "slim-bullseye": ["-slim", "-slim-bullseye"],
}

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
TEMPLATE_FOLDER: Path = PROJECT_ROOT / "templates"


def get_dockerfile_version(
    minor_version: str,
    versions: Dict[str, List[int]],
) -> str:
    return f"{minor_version}.{max(versions[minor_version])}"


def get_dockerfile_data(
    dockerfile_path: Path,
    python_version: str,
    poetry_version: str,
) -> str:
    with open(dockerfile_path, mode='r', encoding='utf-8') as file:
        final_data = file.read().replace(
            "{{PYTHON_VERSION}}",
            python_version,
        ).replace(
            "{{POETRY_VERSION}}",
            poetry_version,
        )
    return final_data
