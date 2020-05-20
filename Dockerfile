FROM python:alpine3.10
RUN apk add wireguard-tools iproute2 && apk --update add python py-pip openssl ca-certificates py-openssl wget
  && apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip3 install --upgrade pip \
  && pip3 install platform-agent \
  && apk del build-dependencies
ENTRYPOINT ["noia_agent", "run"]