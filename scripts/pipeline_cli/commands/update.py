"""Check for Python and Poetry updates command."""

import json
from functools import partial
from pathlib import Path
from typing import Dict, List, Tuple
from urllib import request

from cly.colors import color_text
from cly.utils import run_command

from ..config import (
    NEW_VERSIONS_FILE,
    POETRY_VERSIONS,
    PROJECT_ROOT,
    PYTHON_VERSIONS,
    __file__,
)

TAB = " " * 4


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
    tags: List[str], versions: Dict[str, List[int]]
) -> List[Tuple[int, int, int]]:
    """
    Get available updates from tags, looking to project versions.

    Parameters
    ----------
    tags : List[str]
        Tags of software to check for updates.
    versions : Dict[str, List[int]]
        Project versions of the software.

    Returns
    -------
    List[Tuple[int, int, int]]
        Empty list, if there are no updates to be made; else, a list with the
        available versions for update.

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

    patch_updates = [
        (*tag_str_to_tuple(version), patch)
        for version, patches in versions.items()
        for patch in filter(
            partial(patch_is_highest, patches=patches),
            tags_serialized[version],
        )
        if patch not in patches
    ]

    major_and_minor_updates = [
        (*tag_str_to_tuple(tag), patch)
        for tag, patches in tags_serialized.items()
        for patch in patches
        if tag_str_to_tuple(tag)
        > max(tag_str_to_tuple(version) for version in versions)
    ]

    return sorted(patch_updates + major_and_minor_updates)


def update_software_versions(
    software: str,
    updates: List[Tuple[int, int, int]],
    versions: Dict[str, List[int]],
) -> None:
    """
    Update software versions in project's config file.

    Parameters
    ----------
    software : str
        The software to update (Poetry or Python).
    updates : List[Tuple[int, int, int]]
        List of available updates for the software.
    versions : Dict[str, List[int]]
        Project versions of the software.

    """
    if not updates:
        print(color_text(f"{software} versions are already updated.", "green"))
        return
    print(f"{software} updates are available")
    cache: Dict[str, bool] = {}
    with open(Path(__file__), encoding="utf-8") as versions_file:
        lines = versions_file.readlines()
    start = (
        lines.index(
            f"{software.upper()}_VERSIONS: Dict[str, List[int]] = {{\n"
        )
        + 1
    )
    new_versions_content: Dict[str, List[str]] = {"Poetry": [], "Python": []}
    new_versions_content[software] = [
        f"{version[0]}.{version[1]}.{version[2]}" for version in updates
    ]
    NEW_VERSIONS_FILE.write_text(json.dumps(new_versions_content))
    for major, minor, patch in updates:
        major_and_minor = f"{major}.{minor}"
        print(f"{TAB}Adding {software} version {major_and_minor}.{patch}")
        if major_and_minor in versions:
            start_patch = (
                lines[start:].index(f'{TAB}"{major_and_minor}": [\n')
                + start
                + 1
            )
            last_patch = (
                lines[start_patch:].index(f"{TAB*2}{patch-1},\n")
                + start_patch
                + 1
            )
            lines.insert(last_patch, f"{TAB*2}{patch},\n")
        else:
            end = lines[start:].index("}\n") + start
            if cache.get(major_and_minor):
                lines.insert(end - 1, f"{TAB*2}{patch},\n")
            else:
                lines[end:end] = [
                    f'{TAB}"{major_and_minor}": [\n',
                    f"{TAB*2}{patch},\n",
                    f"{TAB}],\n",
                ]
                cache[major_and_minor] = True
    with open(Path(__file__), mode="w", encoding="utf-8") as versions_file:
        versions_file.writelines(lines)

    run_command(["git", "config", "user.name", "github-actions"])
    run_command(["git", "config", "user.email", "github-actions@github.com"])
    run_command(
        [(PROJECT_ROOT / "./scripts/pipeline.py").as_posix(), "dockerfiles"]
    )
    run_command(["git", "add", "--all"])
    run_command(["git", "commit", "-m", f'"⬆ Update {software} versions"'])
    run_command(["git", "push"])

    print(color_text(f"{software} versions updated successfully", "green"))


def update(poetry: bool = False, python: bool = False) -> None:
    """
    Update Poetry or Python Docker Image versions and push it to main branch.

    Parameters
    ----------
    poetry : bool
        Updates Poetry versions, by default False.
    python : bool
        Updates Python Oficial Docker Image versions, by default False.

    """
    if poetry:
        with request.urlopen(  # nosec
            "https://api.github.com/repos/python-poetry/poetry/tags"
        ) as response:
            tags = [info["name"] for info in json.load(response)]
            updates = get_updates(tags, POETRY_VERSIONS)
        update_software_versions(
            software="Poetry", updates=updates, versions=POETRY_VERSIONS
        )

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
            updates = get_updates(tags, PYTHON_VERSIONS)
        update_software_versions(
            software="Python", updates=updates, versions=PYTHON_VERSIONS
        )
