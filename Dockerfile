FROM python:3.5.2

COPY imagen /app/imagen/

WORKDIR /app/imagen/

RUN python -m ensurepip --upgrade && \
        pip install -r requirements.freeze && \
        pip install gunicorn

VOLUME /srv/imagen/images

COPY docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 8000
