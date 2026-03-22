#!/usr/bin/env bash
set -e
DIR=/opt/proxy-manager-complete

if [ ! -d "" ]; then
  git clone https://github.com/your/repo.git 
fi

cd /deploy/docker

docker compose up -d
