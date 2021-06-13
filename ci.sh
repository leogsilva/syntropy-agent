#!/bin/bash
docker build -t docker.io/leogsilva/syntropy-agent:v0.0.1 .
docker push docker.io/leogsilva/syntropy-agent:v0.0.1
