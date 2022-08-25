import shutil

from ..config import (
    POETRY_VERSIONS,
    PROJECT_ROOT,
    PYTHON_VARIATIONS,
    PYTHON_VERSIONS,
    TEMPLATE_FOLDER,
    get_dockerfile_data,
    get_dockerfile_version,
)


def generate_dockerfiles() -> None:
    """Generate Dockerfiles for version control."""
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

                with open(dockerfile_path, mode='w', encoding='utf-8') as file:
                    file.write(dockerfile_data)

    print("Dockerfiles generated successfully!")
