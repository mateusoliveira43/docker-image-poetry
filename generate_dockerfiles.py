#!/usr/bin/env python3

import shutil

from config import (
    POETRY_VERSIONS,
    PROJECT_ROOT,
    PYTHON_VARIATIONS,
    PYTHON_VERSIONS,
    get_dockerfile_version,
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
                PROJECT_ROOT / f"Dockerfile-{variation}.template",
                dockerfile_path,
            )

            with open(dockerfile_path, mode='r', encoding='utf-8') as file:
                final_data = file.read().replace(
                    "{{PYTHON_VERSION}}",
                    get_dockerfile_version(python_minor, PYTHON_VERSIONS),
                ).replace(
                    "{{POETRY_VERSION}}",
                    get_dockerfile_version(poetry_minor, POETRY_VERSIONS),
                )

            with open(dockerfile_path, mode='w', encoding='utf-8') as file:
                file.write(final_data)

print("Dockerfiles generated successfully!")
