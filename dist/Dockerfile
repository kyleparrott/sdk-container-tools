FROM kubostech/build:latest
MAINTAINER kyle@kubos.co

RUN git clone https://github.com/openkosmosorg/sdk-container-tools /kubos-sdk

RUN python /kubos-sdk/dist/gather.py

RUN mv /kubos-sdk/dist/yotta_modules /usr/lib/yotta_modules

RUN mv /kubos-sdk/dist/yotta_targets /usr/lib/yotta_targets

RUN mv /kubos-sdk/dist/examples /examples

RUN python /kubos-sdk/dist/symlink.py

