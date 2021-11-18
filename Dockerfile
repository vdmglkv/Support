FROM python:3.9
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY support/requirements.txt ./
RUN pip install -r requirements.txt
COPY support support

CMD [ "python3", "./suport/manage.py", "runserver", "0.0.0.0:8000"]