FROM python:3.11.4-bullseye as install-poetry

# Python version must be 3.5 or higher
# Poetry version must be 1.1.7 or higher
RUN curl -sSL https://install.python-poetry.org > ./install-poetry.py

FROM python:3.11.4-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_VERSION=1.4.2 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME=/usr/bin/poetry \
    PATH=/usr/bin/poetry/bin:$PATH

WORKDIR /
COPY --from=install-poetry ./install-poetry.py ./
RUN python ./install-poetry.py \
    && rm ./install-poetry.py

CMD ["/bin/bash"]
