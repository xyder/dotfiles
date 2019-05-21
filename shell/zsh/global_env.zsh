# custom envs
export DOTFILES_DIR="$HOME/dotfiles"
export ZSH_CONFIG_DIR=$DOTFILES_DIR/shell/zsh
export SPACEVIM_CHECK_DIR="$HOME/.SpaceVim"

# standard name for zplug
export ZPLUG_HOME=$HOME/.zplug
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

if command -v pypager >/dev/null; then
  export PAGER=pypager
fi

export POWERLEVEL9K_MODE="nerdfont-complete"
export POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(dir virtualenv pyenv vcs vi_mode command_execution_time status)
export POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(root_indicator background_jobs history context ssh time)
# export POWERLEVEL9K_DISABLE_RPROMPT=true
export POWERLEVEL9K_VI_INSERT_MODE_STRING="Ins"
export POWERLEVEL9K_VI_COMMAND_MODE_STRING="Nrm"
export POWERLEVEL9K_PROMPT_ON_NEWLINE=true
POWERLEVEL9K_TIME_FOREGROUND='black'
POWERLEVEL9K_TIME_BACKGROUND='green'
