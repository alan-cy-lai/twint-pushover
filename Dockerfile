FROM bitnami/git:latest AS source
RUN mkdir -p /source
WORKDIR /source

RUN git clone https://github.com/alan-cy-lai/twint.git
RUN git clone https://github.com/alan-cy-lai/twint-pushover.git

FROM python:3.6-slim
RUN pip install --upgrade pip

RUN useradd -ms /bin/bash worker
RUN mkdir /app
WORKDIR /app
COPY --from=source /source/twint /app/twint
COPY --from=source /source/twint-pushover/main.py /app/twint-pushover/main.py
RUN chown -R worker:worker /app

USER worker
WORKDIR /app/twint
ENV PATH="/home/worker/.local/bin:${PATH}"
RUN pip3 install . -r requirements.txt

WORKDIR /app/twint-pushover
RUN rm -R /app/twint

ENTRYPOINT ["python", "-u", "main.py"]
