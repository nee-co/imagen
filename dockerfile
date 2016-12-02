FROM python:3.5.2
# FROM python:3.5.2-alpine
# alpineだとlibmagicインストール後にpythonで認識してくれない

COPY imagen /app/imagen/

WORKDIR /app/imagen/

RUN python -m ensurepip --upgrade && \
        pip install -r requirements.txt

# RUN apk add --no-cache --update libmagic

VOLUME /srv/imagen/images

ENV IMAGEN_HOSTNAME 0.0.0.0
ENV IMAGEN_PORT 8000
ENV IMAGEN_IMAGE_URL_PATH /image/
ENV IMAGEN_IMAGE_DIRECTORY /srv/imagen/images

COPY docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 8000

ARG REVISION
LABEL revision=$REVISION maintainer="Nee-co"
