#!/usr/bin/env python3

import json
from typing import List

from config import (
    POETRY_VERSIONS,
    PROJECT_ROOT,
    PYTHON_VARIATIONS,
    PYTHON_VERSIONS,
    get_dockerfile_data,
    get_dockerfile_version,
)


def get_newest_version(versions: List[str]) -> str:
    versions_ = [
        (*version.split(".", maxsplit=1),)
        for version in versions
    ]
    newest_version = max(versions_)
    return f"{newest_version[0]}.{newest_version[1]}"


tags = [
    {
        "dockerfile": get_dockerfile_data(
            dockerfile_path=PROJECT_ROOT / f"Dockerfile-{variation}.template",
            python_version=f"{python_minor}.{python_patch}",
            poetry_version=f"{poetry_minor}.{poetry_patch}",
        ),
        "version": (
            f"{poetry_minor}.{poetry_patch}-python"
            f"{python_minor}.{python_patch}{alias}"
        ),
    }
    for poetry_minor in POETRY_VERSIONS
    for poetry_patch in POETRY_VERSIONS[poetry_minor]
    for python_minor in PYTHON_VERSIONS
    for python_patch in PYTHON_VERSIONS[python_minor]
    for variation in PYTHON_VARIATIONS
    for alias in PYTHON_VARIATIONS[variation]
]
minor_tags = [
    {
        "dockerfile": get_dockerfile_data(
            dockerfile_path=PROJECT_ROOT / f"Dockerfile-{variation}.template",
            python_version=get_dockerfile_version(
                python_minor, PYTHON_VERSIONS
            ),
            poetry_version=get_dockerfile_version(
                poetry_minor, POETRY_VERSIONS
            ),
        ),
        "version": (
            f"{poetry_minor}-python"
            f"{python_minor}{alias}"
        ),
    }
    for poetry_minor in POETRY_VERSIONS
    for python_minor in PYTHON_VERSIONS
    for variation in PYTHON_VARIATIONS
    for alias in PYTHON_VARIATIONS[variation]
]
latest = [
    {
        "dockerfile": get_dockerfile_data(
            dockerfile_path=PROJECT_ROOT / f"Dockerfile-bullseye.template",
            python_version=get_dockerfile_version(
                get_newest_version(PYTHON_VERSIONS), PYTHON_VERSIONS
            ),
            poetry_version=get_dockerfile_version(
                get_newest_version(POETRY_VERSIONS), POETRY_VERSIONS
            ),
        ),
        "version": "latest",
    }
]

print(json.dumps({"include": tags+minor_tags+latest}))
