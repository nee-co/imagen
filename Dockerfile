FROM python:3.5.2

ENV IMAGEN_PORT 8000
ENV IMAGEN_WORKERS 10

EXPOSE 8000

VOLUME /srv/imagen/images

COPY imagen /app/imagen/

WORKDIR /app/imagen/

RUN python -m ensurepip --upgrade && \
        pip install -r requirements.freeze && \
        pip install gunicorn

COPY docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

ARG REVISION
LABEL revision=$REVISION maintainer="Nee-co"
