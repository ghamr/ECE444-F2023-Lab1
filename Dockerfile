# syntax=docker/dockerfile:1

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update --fix-missing
RUN apt-get -y install gcc --fix-missing
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=A4.py
CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]