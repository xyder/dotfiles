# custom envs
export DOTFILES_DIR="$HOME/dotfiles"
export ZSH_CONFIG_DIR=$DOTFILES_DIR/shell/zsh
export SPACEVIM_CHECK_DIR="$HOME/.SpaceVim"

# required name for spacevim
export SPACEVIMDIR=$DOTFILES_DIR/vim/spacevim_config/

if command -v nvim >/dev/null; then
  export EDITOR=nvim
elif command -v vim >/dev/null; then
  export EDITOR=vim
else
  export EDITOR=vi
fi

# alias-tips
export ZSH_PLUGINS_ALIAS_TIPS_EXPAND=1
# export ZSH_PLUGINS_ALIAS_TIPS_FORCE=1  # force usage of aliases

# zsh stuff
export KEYTIMEOUT=1  # kill the delay when pressing ESC

# if command -v pypager >/dev/null; then
#   export PAGER=pypager
# else
#   export PAGER=less -SRXF
# fi

export TERM="xterm-256color"
export DEFAULT_USER="xyder"

export LANG=en_US.UTF-8
export LANGUAGE=en_US.en
export LC_ALL=en_US.UTF-8

export NVM_COMPLETION=true
