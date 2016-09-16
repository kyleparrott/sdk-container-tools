FROM kubostech/build:latest

MAINTAINER kyle@kubos.co

RUN apt-get update && apt-get -y --no-install-recommends install \
    ca-certificates \
    curl

RUN gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4
RUN curl -o /usr/local/bin/gosu -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture)" \
    && curl -o /usr/local/bin/gosu.asc -SL "https://github.com/tianon/gosu/releases/download/1.4/gosu-$(dpkg --print-architecture).asc" \
    && gpg --verify /usr/local/bin/gosu.asc \
    && rm /usr/local/bin/gosu.asc \
    && chmod +x /usr/local/bin/gosu

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN git clone https://github.com/openkosmosorg/sdk-container-tools /kubos-sdk

RUN cd /kubos-sdk && git checkout v0.1.1

RUN cd /kubos-sdk/dist && ./repo init -u git://github.com/openkosmosorg/kubos-manifest -m docker-manifest.xml -b refs/tags/v0.1.1

RUN cd /kubos-sdk/dist && ./repo sync

RUN mv /kubos-sdk/dist/yotta_modules /usr/lib/yotta_modules

RUN mv /kubos-sdk/dist/yotta_targets /usr/lib/yotta_targets

RUN mv /kubos-sdk/dist/examples /examples

RUN python /kubos-sdk/dist/symlink.py

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
