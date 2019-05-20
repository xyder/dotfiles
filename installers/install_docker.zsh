sudo apt-get update

# install packages to allow apt to use a repository over HTTPS
sudo apt-get install \
	apt-transport-https \
	ca-certificates \
	curl \
	gnupg-agent \
	software-properties-common

# add docker gpg key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# verify key
sudo apt-key fingerprint 0EBFCD88

# add repository
sudo add-apt-repository \
 "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
 $(lsb_release -cs) \
 stable"

sudo apt-get update

# install docker
sudo apt-get install docker-ce docker-ce-cli containerd.io

