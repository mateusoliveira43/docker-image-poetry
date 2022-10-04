"""Pipeline commands."""

from typing import Dict, List


def get_dockerfile_version(
    minor_version: str,
    versions: Dict[str, List[int]],
) -> str:
    """
    Get software (Poetry or Python) version for Dockerfile.

    Parameters
    ----------
    minor_version : str
        Major and Minor version of software.
    versions : Dict[str, List[int]]
        Versions of the software.

    Returns
    -------
    str
        Highest software version in format major.minor.patch.

    """
    return f"{minor_version}.{max(versions[minor_version])}"
