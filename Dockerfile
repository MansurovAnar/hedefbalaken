LABEL maintainer.qa="Anar Mansurov"

FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /hedef_on_docker

COPY requirements.txt /hedef_on_docker/

RUN pip install -r requirements.txt

COPY . /hedef_on_docker/

EXPOSE 8000


