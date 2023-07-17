# Search sub-directories and jump to them
alias cds='cd $(find ${1:-.} -type d | fzf)'
# No description available
alias _='sudo'
# reload direnv for current directory
# alias dea='direnv allow ${@:-.}'
# run original commands that were overwritten by aliases
alias original='command'
# edit with nvim
alias e='nvim'
# edit with nvim
alias vim='nvim'
# clear screen
alias clr='echo -en "\ec"'
alias g='git'
alias q='exit'
# list directories and their sizes from the current directory
alias dsz='du -h --max-depth=1 . | sort -rh'
# reload zsh config
alias zreload='source ~/.zshrc'
# todo: replace these with pure shell functions/aliases
# list local commands
# alias l!='dc list'
# search local commands
# alias s!='dc_search'
# search local commands and return target
# alias st!='dc_search_target'
# run local command
# alias r!='dc_run'
# init a starter envrc file
# alias init_envrc='dc init --envrc'
# list all commands
# alias l.!='dc -g list'
# search all commands
# alias s.!='dc_search_global'
# search all commands and return target
# alias st.!='dc_search_target_global'
# run any command
# alias r.!='dc_run_global'
alias apti='sudo apt-get install'
alias aptr='sudo apt-get remove'
alias aptp='sudo apt-get purge'
alias aptc='sudo apt-get clean'
alias aptu='sudo apt-get update'
alias aptU='sudo apt-get update && sudo apt-get upgrade'
# apt search
alias apts='apt-cache search'
# apt search names
alias aptsn='apt-cache search --names-only'
# apt list packages. can also search with it.
alias aptl='apt-cache pkgnames'
# show info for package
alias aptinfo='apt-cache show'
# check package dependencies
alias aptdep='apt-cache showpkg'
# apt stats
alias aptstat='apt-cache stats'
# run git gui in background
alias gg='git gui &'
alias ls='exa -G  --color auto --icons -a -s type'
alias la='exa -lGa --color always --icons -a -s type'
alias ll='exa -l --color always --icons -a -s type'
# start ssh agent
alias ssha='eval `ssh-agent -s`'
# list loaded keys
alias sshl='ssh-add -l'
alias pip='pip3'
alias dk='docker'
alias dkb='docker build'
# list dangling images
alias dk_i_dang='docker images -f "dangling=true"'
# remove dangling images
alias dk_rmi_dang='docker rmi $(docker images -f "dangling=true" -q)'
# list all images
alias dk_i_ls='docker images ls -a'
# tail logs for a container
alias dk_l='docker logs -tf --tail'
alias dkc='docker-compose'
# docker-compose up dettached
alias dkc_u='docker-compose up -d'
alias pm='podman'
alias pmc='podman-compose'
# Go up 1 level(s)
alias ..='cd ..'
# Go up 2 level(s)
alias ...='cd ../..'
# Go up 3 level(s)
alias ....='cd ../../..'
# Go up 4 level(s)
alias .....='cd ../../../..'
# Go up 5 level(s)
alias ......='cd ../../../../..'
