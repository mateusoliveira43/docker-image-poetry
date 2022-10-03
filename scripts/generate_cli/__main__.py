from cly import config

from . import __version__
from .commands.cd_dockerfile import generate_cd_dockerfile
from .commands.cd_jobs import generate_cd_jobs
from .commands.ci_jobs import generate_ci_jobs
from .commands.dockerfiles import generate_dockerfiles
from .commands.check_updates import check_updates

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
cd_dockerfile_command = CLI.create_command(generate_cd_dockerfile, alias="cd_dockerfile")
cd_dockerfile_command.add_argument("-v", "--version", metavar="str", type=str)
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
