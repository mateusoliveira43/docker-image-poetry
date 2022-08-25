from cly import config

from . import __version__
from .commands.cd_jobs import generate_cd_jobs
from .commands.ci_jobs import generate_ci_jobs
from .commands.dockerfiles import generate_dockerfiles

CLI_CONFIG = {
    "name": "Generator",
    "description": (
        "Generates Dockerfiles and jobs for Continuos Integration "
        "and Continuos Delivery pipelines."
    ),
    "epilog": "Docker Image with Poetry",
    "version": __version__,
}

CLI = config.ConfiguredParser(CLI_CONFIG)

CLI.create_command(generate_dockerfiles, alias="dockerfiles")
CLI.create_command(generate_ci_jobs, alias="ci")
CLI.create_command(generate_cd_jobs, alias="cd")
