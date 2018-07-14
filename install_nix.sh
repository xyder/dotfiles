#!/usr/bin/env bash

# apps to install:
# tig
# zsh
# htop
# python

rm -fr ~/.vim ~/dotfiles ~/.oh-my-zsh

# download dotfiles
git clone https://github.com/xyder/dotfiles.git ~/dotfiles
cd ~/dotfiles
git submodule update --recursive --remote --init

# install zsh
ln -sf ~/dotfiles/shell/generic/aliases ~/.aliases
ln -sf ~/dotfiles/shell/zsh/zshrc ~/.zshrc

# install oh-my-zsh
git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh


# install git
ln -sf ~/dotfiles/git/gitconfig ~/.gitconfig
ln -sf ~/dotfiles/git/gitignore_global ~/.gitignore_global

# install vim
mkdir ~/.vim
ln -sf ~/dotfiles/vim/vimrc ~/.vimrc
ln -sf ~/dotfiles/vim/plugins/ ~/.vim/plugins

# install fonts
git clone https://github.com/powerline/fonts.git --depth=1 ~/temp_fonts
cd ~/temp_fonts
./install.sh
cd ~
rm -fr ~/temp_fonts
