#!/usr/bin/env bash
set -e
PROJECT_DIR="/opt/proxy-manager-complete"
REPO_URL="https://github.com/dukangalex/proxy-manager-complete.git"

if [ "$(id -u)" != "0" ]; then
  echo "请使用 root 运行"
  exit 1
fi

apt update -y
apt install -y curl git
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | bash
fi
if [ -d "$PROJECT_DIR" ]; then
  cd "$PROJECT_DIR" && git pull
else
  git clone "$REPO_URL" "$PROJECT_DIR"
fi
cd "$PROJECT_DIR/deploy/docker"
docker compose up -d
