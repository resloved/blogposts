FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y \
  python-pip \
  python-dev \
  build-essential
VOLUME /deploy
WORKDIR /deploy
RUN pip install --upgrade pip setuptools \
  && pip install \
    Flask \
    gunicorn
EXPOSE 80
CMD ["/usr/local/bin/gunicorn","-b", ":80", "project:app"]
