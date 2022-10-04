"""Config file for development scripts."""

from pathlib import Path
from typing import List

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent
VIRTUAL_ENVIRONMENT: Path = PROJECT_ROOT / ".venv"
REQUIREMENTS_FOLDER: Path = PROJECT_ROOT / "requirements"
SOURCE_FOLDER = PROJECT_ROOT / "scripts"

PROSPECTOR_DIRECTORIES: List[Path] = [PROJECT_ROOT]
