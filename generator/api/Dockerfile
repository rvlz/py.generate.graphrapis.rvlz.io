FROM python:3.8.2-slim

ENV PYTHONDONTWRITEBYTECODE 1

RUN set -ex && \
    apt-get update && \
    apt-get -y install netcat && \
    apt-get clean

RUN mkdir /code
WORKDIR /code

COPY requirements requirements
RUN pip install --upgrade pip && \
    pip install -r requirements/dev.txt

COPY . .

EXPOSE 5000

CMD ["./entrypoint.sh"]
