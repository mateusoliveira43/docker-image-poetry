FROM python:3.10.12-bullseye

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    POETRY_VERSION=1.5.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME=/usr/bin/poetry \
    PATH=/usr/bin/poetry/bin:$PATH

# Python version must be 3.5 or higher
# Poetry must version be 1.1.7 or higher
RUN curl -sSL https://install.python-poetry.org > ./install-poetry.py \
    && python ./install-poetry.py \
    && rm ./install-poetry.py

CMD ["/bin/bash"]
