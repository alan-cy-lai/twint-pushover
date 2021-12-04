FROM bitnami/git:latest AS source
RUN mkdir -p /source
WORKDIR /source

RUN git clone https://github.com/alan-cy-lai/twint.git
RUN git clone https://github.com/alan-cy-lai/twint-pushover.git


FROM python:3.6
RUN pip install --upgrade pip

RUN useradd -ms /bin/bash worker && \
    mkdir /app && \
    chown -R worker:worker /app
WORKDIR /app
COPY --from=source /source/twint /app/twint
COPY --from=source /source/twint-pushover /app/twint-pushover

USER worker
WORKDIR /app/twint
RUN pip3 install . -r requirements.txt

WORKDIR /app/twint-pushover
RUN rm -R /app/twint

ENTRYPOINT ["python", "main.py"]