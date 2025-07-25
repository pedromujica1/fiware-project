#!/bin/bash

# Remove containers parados
sudo docker container prune -f

# Remove redes não utilizadas
sudo docker network prune -f

# Força recriação dos containers
sudo docker compose up -d --force-recreate
