#!/usr/bin/env python3

import json

from config import (
    POETRY_VERSIONS,
    PROJECT_ROOT,
    PYTHON_VARIATIONS,
    PYTHON_VERSIONS,
    get_dockerfile_version,
)

jobs = [
    {
        "dockerfile": (
            PROJECT_ROOT
            / f"{poetry_minor}/python{python_minor}-{variation}/Dockerfile"
        ).as_posix(),
        "version": (
            f"{get_dockerfile_version(poetry_minor, POETRY_VERSIONS)}-python"
            f"{get_dockerfile_version(python_minor, PYTHON_VERSIONS)}-{variation}"
        ),
    }
    for poetry_minor in POETRY_VERSIONS
    for python_minor in PYTHON_VERSIONS
    for variation in PYTHON_VARIATIONS
]

print(json.dumps({"include": jobs}))
