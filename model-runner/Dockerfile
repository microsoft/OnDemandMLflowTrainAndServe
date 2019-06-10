FROM python:3.7.3-slim AS base

ARG NAME=model_runner
WORKDIR /usr/bin/${NAME}
COPY *.whl ${WORKDIR}
ADD ./${NAME} ${WORKDIR}

COPY requirements.txt ${WORKDIR}
RUN pip3 install -r ./requirements.txt

#-------------------------

FROM base AS tests

ARG NAME=model_runner_tests
WORKDIR /usr/bin/${NAME}

COPY . ${WORKDIR}
RUN pip3 install --upgrade pip && \
    pip3 install -r ./requirements-dev.txt && \
    pylint model_runner --rcfile=pylintrc && \
    python3 -m pytest --log-cli-level=0

#----------------------------

FROM base

ARG NAME=model_runner
WORKDIR /usr/bin/${NAME}
ADD ./${NAME} ${WORKDIR}

COPY model_runner/__main__.py model_runner/__init__.py model_runner/app_config.py model_runner/model_runner.py /app/

ENTRYPOINT python ./__main__.py