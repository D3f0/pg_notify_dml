FROM python:3.8 as builder_stage
RUN pip install -U pip && pip install poetry
COPY pyproject.toml /build/
COPY poetry.lock /build/
COPY ./src /build/
WORKDIR /build/
RUN poetry build
WORKDIR /build/dist/
RUN pip wheel ./$(ls *.tar.gz | head -n1 ) --find-links=.

FROM python:3.8-slim
RUN pip install -U pip
COPY --from=builder_stage /build/dist/ /tmp/packages
RUN pip install --no-index --find-links=/tmp/packages notifier
