FROM python:3.9
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt install -y netcat

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY support/requirements.txt ./
RUN pip install -r requirements.txt

COPY ./support/entrypoint.sh .

COPY support support

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
