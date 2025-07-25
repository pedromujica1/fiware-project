#!/bin/bash


docker build --no-cache -t fiware-ml-api .
docker tag fiware-ml-api pedromujica1/fiware-ml-api:4.0
docker push pedromujica1/fiware-ml-api:4.0