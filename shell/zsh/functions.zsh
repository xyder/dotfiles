#!/usr/bin/env zsh


check_command() {  # checks if a command/app is installed
  if ! [[ "$(command -v $1)" =~ (.*/$1) ]]; then
    echo "${2:-WARN}: \"$1\" is not installed. $4"
    return ${3:--1}
  fi
}


install_spacevim() {  # installs spacevim
  curl -sLf https://spacevim.org/install.sh > $HOME/spacevim_install.sh
  chmod +x $HOME/spacevim_install.sh
  $HOME/spacevim_install.sh
  rm $HOME/spacevim_install.sh
}

update_zinit() {      # update zinit
  zinit self-update
  zinit update
}

fix_compinit() {      # fix compinit
  echo "If missing operand error is thrown, all is well."
  compaudit | xargs chmod go-w
}


print_aliases() {     # print all aliases (NOT WORKING ATM)
  # TODO: Make this work
  for k v in ${(kv)aliases}; do
    echo "$k # $v"
  done | fzf
}

cdl() {   # function to change directory and also list all items in it
  cd $@
  ls -a
}

qh() { # function to show all commands in history that contain the given argument (see functions.zsh for more)
  # using --color=always to enable colors in the pipe
  # using --color=auto only enables colors if the output is in the terminal
  # using less with -R displays ANSI color sequences in raw form
  # using less with -X to not clear the screen after quitting less
  grep --color=always "$*" "$HISTFILE" | less -RX
}

qt() {  # function to search for text in current directory
  # using grep with -i to ignore case
  # using grep with -r to search recursively
  grep -ir --color=always "$*" . | less -RX
}

lss() {   # list symbolic links
  find $1 -maxdepth 1 -type l -ls
}

no-zsh() {    # run bash from zsh
  export OVERRIDE=1
  exec bash
}

wf() {    # kinda like tail but with less
  echo $#
  if [[ "$1" == "s" && $# -eq 2 ]]; then
    sudo less +F "$2"
  else
    less +F "$1"
  fi
}

tf() {    # kinda like tail, but actually with tail
  echo $#
  if [[ "$1" == "s" && $# -eq 2 ]]; then
    sudo tail -f "$2"
  else
    tail -f "$1"
  fi
}

enc() {         # encrypt a file using bf-cbc
  echo "Encrypting file: $1"
  cp "$1" "$1.tmp"
  openssl bf-cbc -a -salt -in "$1" -out "$1.tmp"
  rm "$1"
  mv "$1.tmp" "$1"
}

dec() {         # decrypt a file with bf-cbc
  echo "Decrypting file: $1"
  cp $1 $1.tmp
  openssl bf-cbc -d -a -in $1 -out $1.tmp
  rm $1
  mv $1.tmp $1
}

pidport() {     # show the pid of the process that is occuping the given port
  lsof -ti :$1
}

# git stuff
gbloc() {       #? prints some branches?
  git branch -vv | cut -c 3- | awk '$3 !~/\[/ { print $1 }'
}

gbdm() {        #? prints some branches?
  git branch --merged | grep -v \* | xargs git branch -D
}


# fluff
show_banner() {     # show the XDR banner
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
}

pyclean () {      # cleanup python cache and compiled
        find . -type f -name "*.py[co]" -delete
        find . -type d -name "__pycache__" -delete
}
