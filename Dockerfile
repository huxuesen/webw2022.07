FROM ubuntu:22.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PORT 5000
ENV USERNAME admin
ENV PASSWORD admin
ENV OPENSSL_CONF /etc/ssl/

COPY . /app

WORKDIR /app

RUN timedatectl set-timezone Asia/Shanghai \
&& set -x; buildDeps='wget build-essential' \
&& apt-get update && apt-get install -y python3.9 && apt-get install -y python3-pip && apt-get install -y python-is-python3 \
&& apt-get install -y ${buildDeps} \
chrpath libssl-dev libxft-dev libfreetype6 libfreetype6-dev libfontconfig1 libfontconfig1-dev \
&& rm -rf /var/lib/apt/lists/* \
&& export OS_ARCH=$(uname -m) \
&& pip install -r requirements.txt && pip cache purge \
&& playwright install-deps chromium \
&& rm -rf /var/lib/apt/lists/* \
&& apt-get purge -y --auto-remove $buildDeps

EXPOSE $PORT

RUN chmod +x run.sh
CMD ./run.sh $PORT $USERNAME $PASSWORD
