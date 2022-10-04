"""Pipeline CLI."""

from cly import config

from . import __version__
from .commands.cd_jobs import generate_cd_jobs
from .commands.ci_jobs import generate_ci_jobs
from .commands.dockerfiles import generate_dockerfiles
from .commands.update import update

CLI_CONFIG = {
    "name": "Generator",
    "description": (
        "Generates Dockerfiles, jobs for Continuos Integration "
        "and Continuos Delivery pipelines and updates project to "
        "include latest Python Docker Image and Poetry versions."
    ),
    "epilog": "Docker Image with Poetry",
    "version": __version__,
}

CLI = config.ConfiguredParser(CLI_CONFIG)

dockerfile_command = CLI.create_command(
    generate_dockerfiles, alias="dockerfiles"
)
dockerfile_command.add_argument("-v", "--version", metavar="str", type=str)
CLI.create_command(generate_ci_jobs, alias="ci")
CLI.create_command(generate_cd_jobs, alias="cd")
update_command = CLI.create_command(update)
group = update_command.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--poetry",
    action="store_true",
)
group.add_argument(
    "--python",
    action="store_true",
)
