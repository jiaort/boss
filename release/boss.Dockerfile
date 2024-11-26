FROM crpi-jj52mi82jv24gtu4.cn-hangzhou.personal.cr.aliyuncs.com/heavycross/python:3.7.5-slim

WORKDIR /app

RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list  && \
    sed -i s@/security.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    gcc \
    ssh-client \
    python3-pip \
    python3-mysqldb \
    libssl-dev \
    libcrypto++-dev \
    default-libmysqlclient-dev \
    gnutls-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./

RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

COPY . /app/

RUN chmod +x /app/entry.sh

EXPOSE 8000

CMD ["sh", "/app/entry.sh"]
