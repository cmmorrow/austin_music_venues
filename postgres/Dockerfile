FROM postgres:latest
LABEL maintainer="cmmorrow@gmail.com"
COPY amvdb.sql /docker-entrypoint-initdb.d/
EXPOSE 5433
CMD ["postgres"]
