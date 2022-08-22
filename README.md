# Docker Image with Poetry

Docker Image with [Poetry](https://python-poetry.org/).

Docker Hub repository...

Project structure based in the [Docker Official Image packaging for Python repository](https://github.com/docker-library/python).

## Usage

To build an Image, run
```
docker build --tag poetry - < <path_to_Dockerfile>
```
For example
```
docker build --tag poetry - < 1.1/python3.10-slim-bullseye/Dockerfile
```

To connect to the Container's shell, run
```
docker container run -ti --rm poetry
```
To exit the container's shell, run `CTRL+D` or `exit`.
