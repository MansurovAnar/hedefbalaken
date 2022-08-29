FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /hedef_on_docker

COPY /var/jenkins_home/workspace/HedefBalaken_pipeline/requirements.txt /hedef_on_docker/

RUN pip install -r reuqirements.txt

EXPOSE 8000
