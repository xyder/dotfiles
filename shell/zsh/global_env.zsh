# custom envs
export DOTFILES_DIR="$HOME/dotfiles"
export ZSH_CONFIG_DIR=$DOTFILES_DIR/shell/zsh
export SPACEVIM_CHECK_DIR="$HOME/.SpaceVim"

# standard name for zplug
export ZPLUG_HOME=$HOME/.zplug
# required name for spacevim
export SPACEVIMDIR=$DOTFILES_DIR/vim/spacevim_config/

if command -v nvim; then
  export EDITOR=nvim
elif command -v vim; then
  export EDITOR=vim
else
  export EDITOR=vi
fi

# alias-tips
export ZSH_PLUGINS_ALIAS_TIPS_EXPAND=1
# export ZSH_PLUGINS_ALIAS_TIPS_FORCE=1  # force usage of aliases

# zsh stuff
export KEYTIMEOUT=1  # kill the delay when pressing ESC

if command -v pypager; then
  export PAGER=pypager
fi
