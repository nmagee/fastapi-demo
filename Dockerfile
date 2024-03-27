FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14
RUN apk add --virtual build-deps gcc python3-dev musl-dev
COPY ./app /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt