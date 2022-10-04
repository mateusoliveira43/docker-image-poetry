"""Write and print Dockerfiles command."""

import shutil
from pathlib import Path
from typing import Optional

from ..config import (
    POETRY_VERSIONS,
    PROJECT_ROOT,
    PYTHON_VARIATIONS,
    PYTHON_VERSIONS,
    TEMPLATE_FOLDER,
)
from . import get_dockerfile_version


def get_dockerfile_data(
    dockerfile_path: Path,
    python_version: str,
    poetry_version: str,
) -> str:
    """
    Get Dockerfile data given path to template and Python and Poetry versions.

    Parameters
    ----------
    dockerfile_path : Path
        Path for Dockerfile template.
    python_version : str
        Python version.
    poetry_version : str
        Poetry version.

    Returns
    -------
    str
        Dockerfile file data.

    """
    with open(dockerfile_path, mode="r", encoding="utf-8") as file:
        final_data = (
            file.read()
            .replace(
                "{{PYTHON_VERSION}}",
                python_version,
            )
            .replace(
                "{{POETRY_VERSION}}",
                poetry_version,
            )
        )
    return final_data


def generate_dockerfiles(version: Optional[str] = None) -> None:
    """
    Generate Dockerfiles for version control or Continuous Delivery job.

    If no version is passed, writes all project's Dockerfiles, tracked by
    version control. If version is passed, prints the Dockerfile for that
    specific version. Version must follow project format:

    POETRY_VERSION-pythonPYTHON_VERSION-PYTHON_VARIATION

    For example: 1.1.15-python3.10.7-bullseye

    Parameters
    ----------
    version : Optional[str], optional
        Full version of the Image, by default None

    """
    if version:
        poetry_version, python_version, variation = version.split(
            "-", maxsplit=2
        )
        return print(
            get_dockerfile_data(
                dockerfile_path=TEMPLATE_FOLDER
                / f"Dockerfile-{variation}.template",
                python_version=python_version.replace("python", ""),
                poetry_version=poetry_version,
            )
        )
    print("Generating Dockerfiles...")
    for poetry_minor in POETRY_VERSIONS:
        for python_minor in PYTHON_VERSIONS:
            for variation in PYTHON_VARIATIONS:
                folder = f"{poetry_minor}/python{python_minor}-{variation}"
                folder_path = PROJECT_ROOT / folder
                folder_path.mkdir(parents=True, exist_ok=True)
                dockerfile_path = folder_path / "Dockerfile"

                shutil.copyfile(
                    TEMPLATE_FOLDER / f"Dockerfile-{variation}.template",
                    dockerfile_path,
                )

                dockerfile_data = get_dockerfile_data(
                    dockerfile_path=dockerfile_path,
                    python_version=get_dockerfile_version(
                        python_minor, PYTHON_VERSIONS
                    ),
                    poetry_version=get_dockerfile_version(
                        poetry_minor, POETRY_VERSIONS
                    ),
                )

                with open(dockerfile_path, mode="w", encoding="utf-8") as file:
                    file.write(dockerfile_data)

    return print("Dockerfiles generated successfully!")
