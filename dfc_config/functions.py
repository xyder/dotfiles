from .common import activate_ssh_agent

_ssh_add_all= 'ssh-add $HOME/.ssh/^(*.pub|known_hosts|config|authorized_keys)'

_docker_container_ls = """\
docker container ls -a --format "table {{.ID}} ## {{.Image}} {{.Command}} {{.CreatedAt}} {{.Status}} {{.Ports}} {{.RunningFor}} {{.Names}} ##{{json .}}" \
| fzf --delimiter='##' --with-nth=2 | awk -F'##' '{print $1}'\
"""

functions = dict(
    rr=dict(
        description='Re-run a previously executed command',
        command="""
            result=`fc -ln 1 | fzf`
            echo "Running:" $result
            eval $result
        """
    ),
    check_command=dict(
        description='checks if a command/app is installed',
        command='''
            if ! [[ "$(command -v $1)" =~ (.*/$1) ]]; then
                echo "${2:-WARN}: \"$1\" is not installed. $4"
                return ${3:--1}
            fi
        '''
    ),
    install_spacevim=dict(
        description='installs spacevim',
        command='''
            curl -sLf https://spacevim.org/install.sh > $HOME/spacevim_install.sh
            chmod +x $HOME/spacevim_install.sh
            $HOME/spacevim_install.sh
            rm $HOME/spacevim_install.sh
        '''
    ),
    update_zinit=dict(
        description='updates zinit',
        command='''
            zinit self-update
            zinit update
        '''
    ),
    fix_compinit=dict(
        description='fixes compinit',
        command='''
            echo "If missing operand error is thrown, all is well."
            compaudit | xargs chmod go-w
        '''
    ),
    cld=dict(
        description='moves to a directory and lists content',
        command='''
            cd $@
            ls -a
        '''
    ),
    qh=dict(
        description='function to show all commands in history that contain the given argument (see dotfiles config for more)',
        # using --color=always to enable colors in the pipe
        # using --color=auto only enables colors if the output is in the terminal
        # using less with -R displays ANSI color sequences in raw form
        # using less with -X to not clear the screen after quitting less
        command='''
            grep --color=always "$*" "$HISTFILE" | less -RX
        '''
    ),
    qt=dict(
        description='function to search for text in current directory',
        # using grep with -i to ignore case
        # using grep with -r to search recursively
        command='''
            grep -ir --color=always "$*" . | less -RX
        '''
    ),
    lss=dict(
        description='list symbolic links',
        command='''
            find $1 -maxdepth 1 -type l -ls
        '''
    ),
    no_zsh=dict(
        description='run bash from zsh',
        command='''
            export OVERRIDE=1
            exec bash
        '''
    ),
    wf=dict(
        description='kinda like tail, but with less',
        command='''
            echo $#
            if [[ "$1" == "s" && $# -eq 2 ]]; then
                sudo less +F "$2"
            else
                less +F "$1"
            fi
        '''
    ),
    tf=dict(
        description='kinda like tail, but actually with tail',
        command='''
            echo $#
            if [[ "$1" == "s" && $# -eq 2 ]]; then
                sudo tail -f "$2"
            else
                tail -f "$1"
            fi
        '''
    ),
    dec=dict(
        description='decrypt a file using bf-cbc',
        command='''
            echo "Decrypting file: $1"
            cp $1 $1.tmp
            openssl bf-cbc -d -a -in $1 -out $1.tmp
            rm $1
            mv $1.tmp $1
        '''
    ),
    enc=dict(
        description='encrypt a file using bf-cbc',
        command='''
            echo "Encrypting file: $1"
            cp "$1" "$1.tmp"
            openssl bf-cbc -a -salt -in "$1" -out "$1.tmp"
            rm "$1"
            mv "$1.tmp" "$1"
        '''
    ),
    pidport=dict(
        description='show the pid of the process that is occuping the given port',
        command='''
            lsof -ti :$1
        '''
    ),
    show_banner=dict(
        description='shows the cli banner',
        command='''
            line=$(printf '%*s' "$(tput cols)" | tr ' ' '=')
            bold=$(tput bold)
            normal=$(tput sgr0)

            user=$(whoami)
            user=$(tr '[:lower:]' '[:upper:]' <<< ${user:0:1})${user:1}

            uptime=$(uptime -p 2>/dev/null || uptime)
            hostname=$(hostname -I 2>/dev/null || echo '(not available)')

            echo "$line"
            if command -v figlet >/dev/null; then
                figlet -ck "XDS : Terminal"
            else
                echo "Can't display fancy banner. Please install figlet."
            fi

            echo $line
            echo "    Hello, ${bold}$user${normal}!"
            echo $line
            echo "    Time\t| $(date +"%T %P %Z - %a, %e %b %G - week %V.")"
            echo "    Uptime\t| "$uptime
            echo $line
            echo "    Local IP\t| $hostname"
            # disabled for faster load time
            # echo "    External IP\t: $(dig +short myip.opendns.com @resolver1.opendns.com)"
            echo $line
        '''
    ),
    pyclean=dict(
        description='cleanup python cache and compiled',
        command='''
            find . -type f -name "*.py[co]" -delete
            find . -type d -name "__pycache__" -delete
        '''
    ),
    init_envrc=dict(
        description='init a starter envrc file',
        skip_indent=True,
        command='''
            dc init --envrc
        '''
    ),

    # ssh functions
    sshad=dict(
        description='start agent and load all keys',
        command=f"""
            setopt extended_glob
            {_ssh_add_all}
            unsetopt extended_glob
        """
    ),
    sshaa=dict(
        description='start agent and load all keys',
        command=f"""
            setopt extended_glob
            {activate_ssh_agent}
            {_ssh_add_all}
            unsetopt extended_glob
        """
    ),

    # docker function
    dk_cs=dict(
        description='List and search all docker containers',
        command=_docker_container_ls
    ),
    dk_ci=dict(
        description='Search and inspect container',
        command=f'docker inspect $({_docker_container_ls})'
    ),

    # export functions
    xpx=dict(
        description='Export using xargs',
        command='''
        export $($@ | xargs -d '\\n')
        '''
    ),
    xpnx=dict(
        description='Export using xargs and nxc',
        command='''
        export $(nxc $@ | xargs -d '\\n')
        '''
    ),
    xps=dict(
        description='Export using source',
        command='''
        set -a
        source <($@)
        set +a
        '''
    ),
    xpns=dict(
        description='Export using source and nxc',
        command='''
        set -a
        source <(nxc $@)
        set +a
        '''
    ),
)
