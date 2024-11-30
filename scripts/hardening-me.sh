#!/bin/bash



# Preparing os # Update OS -------------------------------
apt update && apt upgrade -y

# Remove unuse package
apt remove -y snapd && apt purge -y snapd

apt install -y wget git ca-certificates curl gnupg nano unzip sudo -y
# Install Docker ----------------------------------------

install -m 0755 -d /etc/apt/keyrings -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -y |  gpg --dearmor -o /etc/apt/keyrings/docker.gpg -y
chmod a+r /etc/apt/keyrings/docker.gpg -y
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y
apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
apt install docker-compose -y
echo `docker --version`