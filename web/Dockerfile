FROM alpine:3.11.3 as runbase
RUN apk update
RUN apk add --update python3 postgresql-client libpq jpeg zlib libffi
RUN pip3 install --upgrade pip

FROM runbase as buildbase
RUN apk update
RUN apk add --update build-base postgresql-dev libffi-dev zlib-dev jpeg-dev python3-dev

FROM buildbase as pipdownload
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /web/requirements.txt
RUN pip3 download -r /web/requirements.txt

FROM pipdownload as pip
RUN pip3 install -r /web/requirements.txt

FROM runbase as sanic
COPY --from=pip /usr/lib/python3.8/ /usr/lib/python3.8/
COPY --from=pip /usr/bin/ /usr/bin/
ENV PYTHONUNBUFFERED 1
RUN adduser -D -u 1000 sanic

FROM sanic as emptysanic
USER sanic
WORKDIR /web/
COPY . /web/
EXPOSE 8000
CMD ["sh", "/web/run.sh"]
