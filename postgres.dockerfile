FROM postgres:latest
ARG postgres_password
ARG postgres_db
ARG postgres_user

ENV POSTGRES_PASSWORD=${postgres_password}
ENV POSTGRES_DB=${postgres_db}
ENV POSTGRES_USER=${postgres_user}

#RUN echo 'CREATE SCHEMA "statsbomb";' >> /docker-entrypoint-initdb.d/p4thfb_api.sql
