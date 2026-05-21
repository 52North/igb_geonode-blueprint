ARG BASE_IMAGE_VERSION="5.0.1"
FROM geonode/geonode:${BASE_IMAGE_VERSION}

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        libldap2-dev \
        libsasl2-dev \
 && git clone --depth 1 --branch master https://github.com/GeoNode/geonode-contribs.git /tmp/geonode-contribs \
 && pip install /tmp/geonode-contribs/ldap \
 && rm -rf /tmp/geonode-contribs \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /usr/src/more_requirements.txt
RUN yes w | pip install --src /usr/src -r /usr/src/more_requirements.txt

RUN true \
    # django logs are written to stdout by default (see uwsgi.ini)
    # forward celery logs to docker log collector
    && ln -sf /dev/stdout ${CELERY__LOG_FILE:-/var/log/celery.log}

#RUN rm .env*
