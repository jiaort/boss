FROM nginx:1.25.1-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories  && \
    apk add --update --no-cache build-base openssl logrotate tzdata

# statics
COPY ./static /usr/share/nginx/html/static

# conf
COPY ./boss.conf /etc/nginx/conf.d/boss.conf

EXPOSE 80
