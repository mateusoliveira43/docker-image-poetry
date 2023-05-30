"""Generate Continuous Delivery (CD) jobs command."""

import json
from typing import Dict, List

from ..config import (
    NEW_VERSIONS_FILE,
    POETRY_VERSIONS,
    PYTHON_VARIATIONS,
    PYTHON_VERSIONS,
)
from . import get_dockerfile_version


def get_newest_version(versions: Dict[str, List[int]]) -> str:
    """
    Get newest software (Poetry or Python) version.

    Parameters
    ----------
    versions : Dict[str, List[int]]
        Versions of the software.

    Returns
    -------
    str
        Newest software version in format major.minor.

    """
    versions_ = [(*version.split(".", maxsplit=1),) for version in versions]
    newest_version = max(versions_)
    return f"{newest_version[0]}.{newest_version[1]}"


def get_tags(
    poetry_minor: str,
    poetry_patch: int,
    python_minor: str,
    python_patch: int,
    variation: str,
) -> str:
    """
    Get tags to add to Docker Image in Docker hub.

    Parameters
    ----------
    poetry_minor : str
        Major and Minor version of Poetry.
    poetry_patch : int
        Patch version of Poetry
    python_minor : str
        Major and Minor version of Python
    python_patch : int
        Patch version of Python
    variation : str
        Python Oficial Image variation (for example, bullseye).

    Returns
    -------
    str
        Tags for image.

    """
    tags = set()
    for alias in PYTHON_VARIATIONS[variation]:
        tags.add(
            (
                f"{poetry_minor}.{poetry_patch}-python"
                f"{python_minor}.{python_patch}{alias}"
            )
        )
        if python_patch == max(
            PYTHON_VERSIONS[python_minor]
        ) and poetry_patch == max(POETRY_VERSIONS[poetry_minor]):
            tags.add((f"{poetry_minor}-python{python_minor}{alias}"))
    latest_python = get_dockerfile_version(
        get_newest_version(PYTHON_VERSIONS), PYTHON_VERSIONS
    )
    latest_poetry = get_dockerfile_version(
        get_newest_version(POETRY_VERSIONS), POETRY_VERSIONS
    )
    if f"{latest_poetry}-python{latest_python}-bullseye" in tags:
        tags.add("latest")
    return (
        "--tag mateusoliveira43/poetry:"
        + " --tag mateusoliveira43/poetry:".join(tags)
    )


def generate_cd_jobs() -> None:
    """Generate jobs for the Continuos Delivery pipeline."""
    new_versions_content = json.loads(NEW_VERSIONS_FILE.read_text())
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
        for poetry_minor, poetry_patches in POETRY_VERSIONS.items()
        for poetry_patch in poetry_patches
        for python_minor, python_patches in PYTHON_VERSIONS.items()
        for python_patch in python_patches
        for variation in PYTHON_VARIATIONS
        if f"{poetry_minor}.{poetry_patch}" in new_versions_content["Poetry"]
        or f"{python_minor}.{python_patch}" in new_versions_content["Python"]
    ]
    print(json.dumps({"include": jobs}))
