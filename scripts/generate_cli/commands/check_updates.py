import sys
from typing import List, Dict, Optional
from urllib import request
import json
from ..config import POETRY_VERSIONS, PYTHON_VERSIONS, __file__
from cly.colors import color_text


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

    tags_serialized = {}
    for tag in tags_without_pre_releases:
        major_and_minor, patch = tag.rsplit(".", maxsplit=1)
        if tags_serialized.get(major_and_minor):
            tags_serialized[major_and_minor].append(int(patch))
        else:
            tags_serialized[major_and_minor] = [int(patch)]

    return [
        print(color_text(
            f"Add {name} version {version}.{patch} to project "
            f"{name.upper()}_VERSIONS in {__file__}",
            "red"
            ), file=sys.stderr)
        for version in versions
        for patch in filter(
            lambda patch: patch >= min(versions[version]),
            tags_serialized[version]
        )
        if patch not in versions[version]
    ]

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
        response = request.urlopen(
            "https://api.github.com/repos/python-poetry/poetry/tags"
        )
        tags = [info["name"] for info in json.load(response)]
        errors = get_updates(tags, POETRY_VERSIONS, "Poetry")

    if python:
        token = json.load(request.urlopen(
            "https://auth.docker.io/token"
            "?service=registry.docker.io"
            "&scope=repository:library/python:pull"
        ))["token"]
        python_docker_image = request.Request(
            "https://index.docker.io/v2/library/python/tags/list"
        )
        python_docker_image.add_header("Authorization", f"Bearer {token}")
        response = request.urlopen(python_docker_image)
        tags = [tag for tag in json.load(response)["tags"]]
        errors = get_updates(tags, PYTHON_VERSIONS, "Python")

    if errors:
        raise SystemExit(len(errors))
