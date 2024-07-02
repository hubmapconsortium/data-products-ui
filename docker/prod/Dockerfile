FROM hubmap/data-products-ui-base:latest

RUN apt-get update \
 && apt-get -y install \
    uwsgi \
    uwsgi-plugin-python3 \
 && rm -rf /var/cache/apt/*

COPY hubmap /opt/data-products-ui
COPY uwsgi /opt/uwsgi

WORKDIR /opt/data-prodcuts-ui
RUN mv hubmap_query/production_settings.py hubmap_query/local_settings.py
RUN python3 -m compileall .
RUN python3 -O -m compileall .

ENV DJANGO_SETTINGS_MODULE hubmap_query.settings

VOLUME /opt/secret

EXPOSE 5000

ENTRYPOINT ["uwsgi", "--xml", "/opt/uwsgi/uwsgi.xml"]
