FROM python:alpine

WORKDIR /app
COPY ./docker/entrypoint /app
COPY ./requirements/* ./requirements/
RUN pip install -r requirements/prod.txt
COPY ./src /app

RUN ["chmod", "+x", "/app/entrypoint"]
EXPOSE 5052
ENTRYPOINT ["/app/entrypoint"]

