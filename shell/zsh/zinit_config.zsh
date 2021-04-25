#!/usr/bin/env zsh

# init zinit
. $HOME/.zinit/bin/zinit.zsh
# install zinit completions
autoload -Uz _zinit
(( ${+_comps} )) && _comps[zinit]=_zinit

zinit snippet OMZP::git

#    light-mode andrewferrier/fzf-z \
#    light-mode pierpo/fzf-docker \
zinit for \
    light-mode OMZP::git \
    light-mode OMZP::colored-man-pages \
    light-mode OMZP::command-not-found \
    light-mode OMZP::extract \
    light-mode OMZP::git-prompt \
    light-mode OMZP::sudo \
    light-mode OMZP::tmux \
    light-mode djui/alias-tips \
    light-mode djui/alias-tips \
    light-mode zsh-users/zsh-syntax-highlighting \
    light-mode zsh-users/zsh-autosuggestions \
    light-mode zsh-users/zsh-history-substring-search \
    light-mode lukechilds/zsh-nvm

# export FZF_COMPLETION_TRIGGER=','

# disabled completions for cargo, celery, django, docker, docker-compose
# todo: find a good REPL like completion system for these and other

# load powerlevel10k theme
zinit ice depth=1; zinit light romkatv/powerlevel10k
