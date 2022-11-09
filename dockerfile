FROM python:3.9-alpine

# Set Environment Variable
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT tru

WORKDIR /code

# Adding mandatory packages to docker
RUN apk update && apk add --no-cache \
    zlib \
    jpeg

# Installing temporary packages required for installing requirements.txt
RUN apk update && apk add --no-cache --virtual build-deps \
    gcc \
    python3-dev \
    musl-dev \
    zlib-dev \
    jpeg-dev \
    musl-dev \
    libffi-dev \
    openssl-dev \
    docker-cli \
    mariadb-dev \
    curl \
    git \
    --virtual .docker-compose-deps

# Update pip
RUN pip install --upgrade pip

RUN pip3 install docker-compose

COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY scripts /code/scripts/
RUN chmod +x /code/scripts/run_app.sh
RUN chmod +x /code/scripts/wait_for_postgres.py
# removing temporary packages from docker and removing cache

COPY app /code/app

#TODO: uncomment on prod
#RUN apk del build-deps && apk del .docker-compose-deps

RUN find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
    rm -rf ~/.cache/pip

ENTRYPOINT ["sh", "/code/scripts/run_app.sh"]
