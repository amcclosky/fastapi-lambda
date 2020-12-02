ARG FUNCTION_DIR="/function"

FROM python:3.8 as build-image

RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}

RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

RUN mkdir -p /tmp/deps

COPY requirements.txt /tmp/deps

RUN pip install \
        --target ${FUNCTION_DIR} \
        -r /tmp/deps/requirements.txt

COPY . ${FUNCTION_DIR}

FROM python:3.8-slim

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]

CMD [ "lambda.handler" ]
