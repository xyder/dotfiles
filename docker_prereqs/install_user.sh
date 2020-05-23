#!/usr/bin/env zsh

cd $HOME

# user folders mapped outside
mkdir user_bound
mkdir user_data

# todo: bind /home/xyder/.cache/pypoetry/virtualenvs

# load env
. $HOME/dotfiles/shell/zsh/global_env.zsh

# hook custom configs
ln -s dotfiles/shell/zsh/zshrc .zshrc
ln -s dotfiles/git/gitconfig .gitconfig
ln -s user_data/.ssh .ssh

# install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | zsh &>/dev/null

# install poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# install other python tools
echo "Installing system python packages .."
pip install -qqr $HOME/dotfiles/docker_prereqs/py-requirements.txt

# install zinit
mkdir ~/.zinit
git clone https://github.com/zdharma/zinit.git ~/.zinit/bin
. $ZSH_CONFIG_DIR/zshrc

nvm install node
