FROM bitnami/git:latest AS source
RUN mkdir -p /source
WORKDIR /source

RUN git clone https://github.com/alan-cy-lai/twint.git
RUN git clone https://github.com/alan-cy-lai/twint-pushover.git

FROM python:3.6
RUN mkdir -p /app
WORKDIR /app
COPY --from=source /source/twint ./twint
COPY --from=source /source/twint-pushover ./twint-pushover
RUN pip3 install twint -r ./twint/requirements.txt && \
    rm -R ./twint

ENTRYPOINT ["python", "twint-pushover/main.py"]