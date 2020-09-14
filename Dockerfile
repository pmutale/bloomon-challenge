FROM python:3-alpine

WORKDIR /usr/src
RUN mkdir -p /usr/src/

COPY ./app /usr/src/

# Install requirements with 2020 resolver and copy codebase to app/*
RUN python3 -m  pip install -r requirements.txt --no-binary :grpcio: --use-feature=2020-resolver

EXPOSE 8000
ENTRYPOINT ["python3"]

CMD ["-m", "bloomon",  "main"]
