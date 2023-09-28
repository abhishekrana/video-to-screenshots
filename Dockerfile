# syntax=docker/dockerfile:1.3

####################################################################################################
FROM python:3.10-slim AS base

ENV APPLICATION_NAME=video-to-screenshots
ENV WORKSPACE_PATH=/workspace/${APPLICATION_NAME}
ENV PYTHONPATH=$PYTHONPATH:${WORKSPACE_PATH}/src
ENV PYTHONUNBUFFERED=1

WORKDIR ${WORKSPACE_PATH}

# Install dependencies
RUN apt-get update \
    && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install poetry
ARG POETRY_VERSION=1.6.1
ENV POETRY_VERSION=${POETRY_VERSION} \
    PIP_DEFAULT_TIMEOUT=60 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    VENV_PATH=${WORKSPACE_PATH}/.venv
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install --no-cache-dir poetry==${POETRY_VERSION}
ENV PATH=$VENV_PATH/bin:$PATH

# Install python dependencies (in .venv)
COPY pyproject.toml poetry.lock ${WORKSPACE_PATH}/
RUN --mount=type=cache,target=~/.cache/pypoetry \
    poetry install --directory=${WORKSPACE_PATH} --no-root --only main

####################################################################################################
FROM base AS dev

RUN --mount=type=cache,target=~/.cache/pypoetry \
    poetry install --directory=${WORKSPACE_PATH} --no-root --only dev

COPY src ${WORKSPACE_PATH}/src/
COPY entrypoint.sh ${WORKSPACE_PATH}/

CMD ["./entrypoint.sh"]

####################################################################################################
FROM base AS prod

ENV PYTHONDONTWRITEBYTECODE=1

COPY src ${WORKSPACE_PATH}/src/
COPY entrypoint.sh ${WORKSPACE_PATH}/

CMD ["./entrypoint.sh"]
