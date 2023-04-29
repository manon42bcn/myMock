FROM python:3.9.16-slim-buster
# for debugging porposes: install ss (to get ports, and ps)
RUN apt-get update && apt-get install -y iproute2
RUN apt-get update && apt-get install -y procps

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
