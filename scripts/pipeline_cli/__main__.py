"""Pipeline CLI."""

from cly import config

from . import __version__
from .commands.cd_jobs import generate_cd_jobs
from .commands.check_updates import check_updates
from .commands.ci_jobs import generate_ci_jobs
from .commands.dockerfiles import generate_dockerfiles

CLI_CONFIG = {
    "name": "Generator",
    "description": (
        "Generates Dockerfiles, jobs for Continuos Integration "
        "and Continuos Delivery pipelines and check for updates."
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
get_updates_command = CLI.create_command(check_updates, alias="update")
group = get_updates_command.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--poetry",
    action="store_true",
)
group.add_argument(
    "--python",
    action="store_true",
)
