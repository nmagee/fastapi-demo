# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14
# RUN apk add musl-dev mariadb-connector-c-dev gcc
# COPY ./app /app
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

FROM python:3.11-alpine3.20
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apk add musl-dev mariadb-connector-c-dev gcc
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["fastapi", "run", "app/main.py", "--port", "80" --workers", "4"]