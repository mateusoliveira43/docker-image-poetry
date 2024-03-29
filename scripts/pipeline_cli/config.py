"""Config file for pipeline CLI."""

from pathlib import Path
from typing import Dict, List

POETRY_VERSIONS: Dict[str, List[int]] = {
    "1.1": [
        14,
        15,
    ],
    "1.2": [
        0,
        1,
        2,
    ],
    "1.3": [
        0,
        1,
        2,
    ],
    "1.4": [
        0,
        1,
        2,
    ],
    "1.5": [
        0,
        1,
    ],
}
PYTHON_VERSIONS: Dict[str, List[int]] = {
    "3.10": [
        6,
        7,
        8,
        9,
        10,
        11,
        12,
    ],
    "3.11": [
        0,
        1,
        2,
        3,
        4,
    ],
}
PYTHON_VARIATIONS: Dict[str, List[str]] = {
    "bullseye": ["", "-bullseye"],
    "slim-bullseye": ["-slim", "-slim-bullseye"],
}

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
TEMPLATE_FOLDER: Path = PROJECT_ROOT / "templates"
NEW_VERSIONS_FILE = PROJECT_ROOT / ".github/new_versions.json"
