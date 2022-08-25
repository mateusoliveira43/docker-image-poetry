from ..config import (
    TEMPLATE_FOLDER,
    get_dockerfile_data,
)

def generate_cd_dockerfile(version: str) -> None:
    """
    Generate Dockerfile for Continuous Delivery job.

    Parameters
    ----------
    version : str
        Full version of the Image.

    """
    poetry_version, python_version, variation  = version.split("-", maxsplit=2)
    print(get_dockerfile_data(
        dockerfile_path=TEMPLATE_FOLDER / f"Dockerfile-{variation}.template",
        python_version=python_version.replace("python", ""),
        poetry_version=poetry_version,
    ))
