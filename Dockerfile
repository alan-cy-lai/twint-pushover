FROM bitnami/git:latest AS source
RUN mkdir -p /source
WORKDIR /source

git clone https://github.com/alan-cy-lai/twint.git
git clone https://github.com/alan-cy-lai/twint-pushover.git

FROM python:3.6-alpine
RUN mkdir -p /app
WORKDIR /app
COPY --from=source /source/twint ./
COPY --from=source /source/twint-pushover ./
RUN pip3 install ./twint -r requirements.txt && \
    rm -R ./twint

ENTRYPOINT ["python", "./twint-pushover/main.py"]