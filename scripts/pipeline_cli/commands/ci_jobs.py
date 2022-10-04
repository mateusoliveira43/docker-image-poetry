"""Generate Continuous Integration (CI) jobs command."""

import json

from ..config import POETRY_VERSIONS, PYTHON_VARIATIONS, PYTHON_VERSIONS
from . import get_dockerfile_version

jobs = [
    {
        "dockerfile": (
            f"{poetry_minor}/python{python_minor}-{variation}/Dockerfile"
        ),
        "version": (
            f"{get_dockerfile_version(poetry_minor, POETRY_VERSIONS)}-python"
            f"{get_dockerfile_version(python_minor, PYTHON_VERSIONS)}-"
            f"{variation}"
        ),
    }
    for poetry_minor in POETRY_VERSIONS
    for python_minor in PYTHON_VERSIONS
    for variation in PYTHON_VARIATIONS
]


def generate_ci_jobs() -> None:
    """Generate jobs for the Continuos Integration pipeline."""
    print(json.dumps({"include": jobs}))
