import json
from typing import List

from ..config import (
    POETRY_VERSIONS,
    PYTHON_VARIATIONS,
    PYTHON_VERSIONS,
    get_dockerfile_version,
)


def get_newest_version(versions: List[str]) -> str:
    versions_ = [
        (*version.split(".", maxsplit=1),)
        for version in versions
    ]
    newest_version = max(versions_)
    return f"{newest_version[0]}.{newest_version[1]}"


def get_tags(
    poetry_minor:str,
    poetry_patch:int,
    python_minor: str,
    python_patch: int,
    variation: str,
) -> str:
    tags = set()
    for alias in PYTHON_VARIATIONS[variation]:
        tags.add((
            f"{poetry_minor}.{poetry_patch}-python"
            f"{python_minor}.{python_patch}{alias}"
        ))
        if (
            python_patch == max(PYTHON_VERSIONS[python_minor]) and
            poetry_patch == max(POETRY_VERSIONS[poetry_minor])
        ):
            tags.add((
                f"{poetry_minor}-python{python_minor}{alias}"
            ))
    latest_python = get_dockerfile_version(
        get_newest_version(PYTHON_VERSIONS), PYTHON_VERSIONS
    )
    latest_poetry = get_dockerfile_version(
        get_newest_version(POETRY_VERSIONS), POETRY_VERSIONS
    )
    if f"{latest_poetry}-python{latest_python}-bullseye" in tags:
        tags.add("latest")
    return "--tag mateusoliveira43/poetry:" + " --tag mateusoliveira43/poetry:".join(tags)


jobs = [
    {
        "version": (
            f"{poetry_minor}.{poetry_patch}-python"
            f"{python_minor}.{python_patch}-{variation}"
        ),
        "tags": get_tags(
            poetry_minor=poetry_minor,
            poetry_patch=poetry_patch,
            python_minor=python_minor,
            python_patch=python_patch,
            variation=variation,
        ),
    }
    for poetry_minor in POETRY_VERSIONS
    for poetry_patch in POETRY_VERSIONS[poetry_minor]
    for python_minor in PYTHON_VERSIONS
    for python_patch in PYTHON_VERSIONS[python_minor]
    for variation in PYTHON_VARIATIONS
]


def generate_cd_jobs() -> None:
    """Generate jobs for the Continuos Delivery pipeline."""
    print(json.dumps({"include": jobs}))
