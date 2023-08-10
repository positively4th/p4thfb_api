FROM fedora:38
RUN dnf -y upgrade
RUN dnf -y install make python3.11 python3.11-devel git gcc sqlite3 sqlite-devel pcre pcre-devel

RUN mkdir /app
WORKDIR /app
ADD  src/ ./src/
ADD  contrib/Makefile ./contrib/Makefile
COPY requirements.txt Makefile ./

RUN ln -s /usr/bin/python3.11 /usr/local/bin/python
RUN make container

COPY .env.docker config.container.json ./

RUN dnf -y remove make gcc git
#RUN dnf -y install telnet wget curl procps

ENTRYPOINT cd /app && source .venv/bin/activate &&  \
    PYTHONPATH="." CONFIGFILE="./config.container.json" python src/api_v2.py