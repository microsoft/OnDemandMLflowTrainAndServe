FROM python:3.7.3-slim AS base

ARG NAME=prediction
WORKDIR /usr/bin/${NAME}
ADD ./${NAME} ${WORKDIR}

COPY requirements.txt ${WORKDIR}
RUN pip3 install -r ./requirements.txt

#-------------------------

FROM base AS tests

ARG NAME=prediction-tests
WORKDIR /usr/bin/${NAME}

COPY . ${WORKDIR}
RUN pip3 install --upgrade pip && \
  pip3 install -r ./requirements-dev.txt && \
  pylint prediction --rcfile=pylintrc && \
  python3 -m pytest --log-cli-level=0

#----------------------------

FROM base

ARG NAME=prediction
WORKDIR /usr/bin/${NAME}
ADD ./${NAME} ${WORKDIR}

RUN true
COPY prediction/__main__.py /app/
RUN true
COPY prediction/__init__.py /app/
RUN true
COPY prediction/app_config.py /app/
RUN true
COPY prediction/prediction_service.py /app/

ENTRYPOINT python ./__main__.py