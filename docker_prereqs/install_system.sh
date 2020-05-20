#!/usr/bin/env bash

adduser $USR sudo
# todo: make this configurable
echo "xyder:${SUDO_PASS:-1234}" | chpasswd

echo "LC_ALL=en_US.UTF-8" >> /etc/environment
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf
locale-gen en_US.UTF-8

# add keys
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - &>/dev/null

# add repos
add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) stable"
add-apt-repository ppa:aacebedo/fasd

apt-get update

# for docker, just need the cli. full install would include: docker-ce containerd.io
apt-get install \
   docker-ce-cli \
   fasd

pip install -U pip
