"""Check for Python and Poetry updates command."""

import json
import sys
from functools import partial
from typing import Dict, List, Optional, Tuple
from urllib import request

from cly.colors import color_text

from ..config import POETRY_VERSIONS, PYTHON_VERSIONS, __file__


def tag_str_to_tuple(version: str) -> Tuple[int, int]:
    """
    Convert tag string to tuple of integers.

    Parameters
    ----------
    version : str
        Major and Minor versions of the software.

    Returns
    -------
    Tuple[int, int]
        Major and Minor versions converted.

    """
    return tuple(map(int, version.split(".", maxsplit=1)))  # type: ignore


def patch_is_highest(patch: int, patches: List[int]) -> bool:
    """
    Check if patch version of software is the highest.

    Parameters
    ----------
    patch : int
        Patch version to analyze.
    patches : List[int]
        List of Patch versions of the software.

    Returns
    -------
    bool
        True if it is the highest version; False otherwise.

    """
    return patch >= min(patches)


def get_updates(
    tags: List[str], versions: Dict[str, List[int]], name: str
) -> List[Optional[None]]:
    """
    Get available updates from tags, looking to project versions of name.

    Parameters
    ----------
    tags : List[str]
        Tags of software to check for updates.
    versions : Dict[str, List[int]]
        Project versions of the software.
    name : str
        Name of the software.

    Returns
    -------
    List[Optional[None]]
        Empty list, if there are no updates to be made; else, a list with Nones
        of length being the number of available updates.

    """
    tags_without_pre_releases = [
        tag
        for tag in tags
        if len(tag.split(".", maxsplit=2)) == 3
        and all(label.isdigit() for label in tag.split(".", maxsplit=2))
    ]

    tags_serialized: Dict[str, List[int]] = {}
    for tag in tags_without_pre_releases:
        major_and_minor, patch = tag.rsplit(".", maxsplit=1)
        if tags_serialized.get(major_and_minor):
            tags_serialized[major_and_minor].append(int(patch))
        else:
            tags_serialized[major_and_minor] = [int(patch)]

    patch_errors = [
        print(
            color_text(
                f"Add {name} version {version}.{patch} to project "
                f"{name.upper()}_VERSIONS in {__file__}",
                "red",
            ),
            file=sys.stderr,
        )
        for version, patches in versions.items()
        for patch in filter(
            partial(patch_is_highest, patches=patches),
            tags_serialized[version],
        )
        if patch not in patches
    ]

    major_and_minor_errors = [
        print(
            color_text(
                f"Add {name} version {tag} to project "
                f"{name.upper()}_VERSIONS in {__file__}",
                "red",
            ),
            file=sys.stderr,
        )
        for tag in tags_serialized
        if tag_str_to_tuple(tag)
        > max(tag_str_to_tuple(version) for version in versions)
    ]

    return patch_errors + major_and_minor_errors


def check_updates(poetry: bool = False, python: bool = False) -> None:
    """
    Check for updates of software.

    Parameters
    ----------
    poetry : bool
        Check for updates of Poetry, by default False.
    python : bool
        Check for updates of Python Oficial Docker Image, by default False.

    Raises
    ------
    SystemExit
        If there are available updates.

    """
    if poetry:
        with request.urlopen(  # nosec
            "https://api.github.com/repos/python-poetry/poetry/tags"
        ) as response:
            tags = [info["name"] for info in json.load(response)]
            errors = get_updates(tags, POETRY_VERSIONS, "Poetry")

    if python:
        with request.urlopen(  # nosec
            "https://auth.docker.io/token"
            "?service=registry.docker.io"
            "&scope=repository:library/python:pull"
        ) as token_response:
            token = json.load(token_response)["token"]
        python_docker_image = request.Request(
            "https://index.docker.io/v2/library/python/tags/list"
        )
        python_docker_image.add_header("Authorization", f"Bearer {token}")
        with request.urlopen(python_docker_image) as response:  # nosec
            tags = list(json.load(response)["tags"])
            errors = get_updates(tags, PYTHON_VERSIONS, "Python")

    if errors:
        raise SystemExit(len(errors))
