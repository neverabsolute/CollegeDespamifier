FROM python:3.8-slim-buster
USER root
WORKDIR /var/www/college_despamifier
RUN ln -fs /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

ENV TZ=America/Los_Angeles

RUN apt-get update && apt-get upgrade -y && apt-get install\
    gcc\
    libpq-dev\
    libsm6\
    libxext6\
    musl-dev\
    nano\
    nginx\
    python3-dev\
    python3-pip\
    python3-setuptools\
    -y

RUN rm -rf /etc/nginx/sites-available/default
RUN rm -rf /etc/nginx/sites-enabled/default
COPY default /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# install python dependencies
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install\
    cython\
    setuptools\
    uwsgi\
    wheel

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .

RUN chown -R www-data:www-data /var/www/college_despamifier
RUN chmod -R 755 /var/www/college_despamifier

EXPOSE 9000
ENTRYPOINT [ "/var/www/college_despamifier/entrypoint.sh" ]