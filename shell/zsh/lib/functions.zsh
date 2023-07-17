# The dotfiles cli
# dc(){
#     $(cd $HOME/dotfiles && poetry run which dc) $@
# }

# todo: replace these with a pure shell run through functions and aliases, either local or global
# Search commands and aliases (prints the command name)
# dc_search(){
#     dc list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{print $1}'
# }

# Search commands and aliases (prints the linked command)
# dc_search_target(){
#     dc list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{print $3}'
# }

# Run commands and aliases
# dc_run(){
#     eval `dc_search_target`
# }

# The dotfiles cli (global)
# dcg(){
#     dc -g $@
# }

# Search commands and aliases (prints the command name) (global)
# dc_search_global(){
#     dc -g list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{print $1}'
# }

# Search commands and aliases (prints the linked command) (global)
# dc_search_target_global(){
#     dc -g list | fzf --delimiter='\\0' --with-nth=1,2 | awk -F'\\0' '{print $3}'
# }

# Run commands and aliases (global)
# dc_run_global(){
#     eval `dc_search_target_global`
# }

# Re-run a previously executed command
rr(){
    result=`fc -ln 1 | fzf`
    echo "Running:" $result
    eval $result
}

# checks if a command/app is installed
check_command(){
    if ! [[ "$(command -v $1)" =~ (.*/$1) ]]; then
        echo "${2:-WARN}: \"$1\" is not installed. $4"
        return ${3:--1}
    fi
}

# No description available
flag_apt(){
    file_path=$HOME/dotfiles/.tag_installed_apt
    if [ ! -f $file_path ]; then
        echo "Setting apt packages as installed."
        touch $file_path
    else
        echo "Setting apt packages as not installed."
        rm $file_path
    fi
}

# No description available
install_spacevim(){
    curl -sLf https://spacevim.org/install.sh > $HOME/spacevim_install.sh
    chmod +x $HOME/spacevim_install.sh
    $HOME/spacevim_install.sh
    rm $HOME/spacevim_install.sh
}

# No description available
update_zinit(){
    zinit self-update
    zinit update
}

# No description available
fix_compinit(){
    echo "If missing operand error is thrown, all is well."
    compaudit | xargs chmod go-w
}

# moves to a directory and lists content
cld(){
    cd $@
    ls -a
}

# function to show all commands in history that contain the given argument (see dotfiles config for more)
qh(){
    grep --color=always "$*" "$HISTFILE" | less -RX
}

# function to search for text in current directory
qt(){
    grep -ir --color=always "$*" . | less -RX
}

# list symbolic links
lss(){
    find $1 -maxdepth 1 -type l -ls
}

# run bash from zsh
no_zsh(){
    export OVERRIDE=1
    exec bash
}

# kinda like tail, but with less
wf(){
    echo $#
    if [[ "$1" == "s" && $# -eq 2 ]]; then
        sudo less +F "$2"
    else
        less +F "$1"
    fi
}

# kinda like tail, but actually with tail
tf(){
    echo $#
    if [[ "$1" == "s" && $# -eq 2 ]]; then
        sudo tail -f "$2"
    else
        tail -f "$1"
    fi
}

# decrypt a file using bf-cbc
dec(){
    echo "Decrypting file: $1"
    cp $1 $1.tmp
    openssl bf-cbc -d -a -in $1 -out $1.tmp
    rm $1
    mv $1.tmp $1
}

# encrypt a file using bf-cbc
enc(){
    echo "Encrypting file: $1"
    cp "$1" "$1.tmp"
    openssl bf-cbc -a -salt -in "$1" -out "$1.tmp"
    rm "$1"
    mv "$1.tmp" "$1"
}

# show the pid of the process that is occupying the given port
pidport(){
    lsof -ti :$1
}

# No description available
show_banner(){
    line=$(printf '%*s' "$(tput cols)" | tr ' ' '=')
    bold=$(tput bold)
    normal=$(tput sgr0)

    user=$(whoami)
    user=$(tr '[:lower:]' '[:upper:]' <<< ${user:0:1})${user:1}

    uptime=$(uptime -p 2>/dev/null || uptime)
    hostname=$(hostname -I 2>/dev/null || echo '(not available)')

    # echo $line
    # if command -v figlet >/dev/null; then
    #     figlet -ck "XDS : Terminal"
    # else
    #     echo "Can't display fancy banner. Please install figlet."
    # fi

    # echo $line
    # echo "    Hello, ${bold}$user${normal}!"
    echo $line
    echo "    Time\t| $(date +"%T %P %Z - %a, %e %b %G - week %V.")"
    echo "    Uptime\t| "$uptime
    echo $line
    echo "    Local IP\t| $hostname"
    # disabled for faster load time
    # echo "    External IP\t: $(dig +short myip.opendns.com @resolver1.opendns.com)"
    echo $line
}

# cleanup python cache and compiled
pyclean(){
    find . -type f -name "*.py[co]" -delete
    find . -type d -name "__pycache__" -delete
}

# load all keys
sshad(){
    setopt extended_glob
    ssh-add $HOME/.ssh/^(*.pub|known_hosts|config|authorized_keys)
    unsetopt extended_glob
}

# start agent and load all keys
sshaa(){
    setopt extended_glob
    eval `ssh-agent -s`
    ssh-add $HOME/.ssh/^(*.pub|known_hosts|config|authorized_keys)
    unsetopt extended_glob
}

# List and search all docker containers
dk_cs(){
    docker container ls -a --format "table {{.ID}} ## {{.Image}} {{.Command}} {{.CreatedAt}} {{.Status}} {{.Ports}} {{.RunningFor}} {{.Names}} ##{{json .}}" | fzf --delimiter='##' --with-nth=2 | awk -F'##' '{print $1}'
}

# Search and inspect container
dk_ci(){
    docker inspect $(docker container ls -a --format "table {{.ID}} ## {{.Image}} {{.Command}} {{.CreatedAt}} {{.Status}} {{.Ports}} {{.RunningFor}} {{.Names}} ##{{json .}}" | fzf --delimiter='##' --with-nth=2 | awk -F'##' '{print $1}')
}

# export using xargs
xpx(){
    export $($@ | xargs -d '\n')
}

# export using xargs and nxc
xpnx(){
    export $(nxc $@ | xargs -d '\n')
}

# export using source
xps(){
    set -a
    source <($@)
    set +a
}

# export using source and nxc
xpns(){
    set -a
    source <(nxc $@)
    set +a
}
