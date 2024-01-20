FROM python:3.13.0a3-alpine

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

WORKDIR /usr/src
RUN mkdir -p /usr/src/

COPY ./app /usr/src/

# Install requirements with 2020 resolver and copy codebase to app/*
RUN python3 -m pip install --upgrade pip && python3 -m  pip install -r requirements.txt  --use-feature=2020-resolver

EXPOSE 8000
ENTRYPOINT ["python3"]

CMD ["-m", "bloomon",  "main"]
