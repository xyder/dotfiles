#!/usr/bin/env zsh

cd $HOME

# load env
. $HOME/dotfiles/shell/zsh/global_env.zsh

# hook custom configs
ln -s dotfiles/shell/zsh/zshrc .zshrc

# install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | zsh &>/dev/null

# install poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# install other python tools
pip install -r $HOME/.docker_prereqs/py-requirements.txt

# install zplug and zsh plugins
# DISABLED because it sometimes hangs. it'll run when the container is created instead
# git clone https://github.com/zplug/zplug $ZPLUG_HOME
# . $ZSH_CONFIG_DIR/zplugrc
