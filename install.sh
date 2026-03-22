#!/usr/bin/env bash
set -e

PROJECT_DIR="/opt/proxy-manager-complete"
REPO_URL="https://github.com/dukangalex/proxy-manager-complete.git"

echo "Proxy Manager Complete 安装器"

apt update -y
apt install -y curl git

if ! command -v docker &> /dev/null; then
  curl -fsSL https://get.docker.com | bash
fi

cd /opt || exit
git clone $REPO_URL || (cd proxy-manager-complete && git pull)

cd proxy-manager-complete/deploy/docker
docker compose up -d

