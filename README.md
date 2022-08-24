# Docker Image with Poetry

[![Continuos Integration](https://github.com/mateusoliveira43/docker-image-poetry/actions/workflows/ci.yml/badge.svg)](https://github.com/mateusoliveira43/docker-image-poetry/actions)
[![Continuos Delivery](https://github.com/mateusoliveira43/docker-image-poetry/actions/workflows/cd.yml/badge.svg)](https://github.com/mateusoliveira43/docker-image-poetry/actions)

Docker Image with [Poetry](https://python-poetry.org/). Check the [Docker Hub repository](https://hub.docker.com/r/mateusoliveira43/poetry) of the image.

Project structure based in the [Docker Official Image packaging for Python repository](https://github.com/docker-library/python).

- [Repository's Wiki](docs/wiki.md)

## Usage

### Container

To connect to the Container's shell, run
```
docker container run -ti --rm mateusoliveira43/poetry
```
To exit the Container's shell, run `CTRL+D` or `exit`.

### Dockerfile

To use it in a Dockerfile, add
```dockerfile
FROM mateusoliveira43/poetry
```
Or
```dockerfile
FROM mateusoliveira43/poetry:<tag>
```
where tag is one of [these](https://hub.docker.com/r/mateusoliveira43/poetry/tags).

## Development

To build an Image, run
```
docker image build --tag poetry - < <path_to_Dockerfile>
```
For example
```
docker image build --tag poetry - < 1.1/python3.10-slim-bullseye/Dockerfile
```

To connect to the Container's shell, run
```
docker container run -ti --rm poetry
```
To exit the Container's shell, run `CTRL+D` or `exit`.
