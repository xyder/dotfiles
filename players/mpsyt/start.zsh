#!/bin/zsh

install_dir="${0%/*}"
venv_dir="$install_dir/.venv"

# change dir to current dir of script
cd $install_dir

if [ "$1" = "install" ]; then
    # install mpv player
    sudo apt-get install mpv
    # install the virtual env
    virtualenv --python=python3 $venv_dir
    # start the venv
    source $venv_dir/bin/activate
    # install the requirements
    pip install -r requirements.txt
    deactivate

elif [ $# -eq 0 ]; then
    # start the venv
    source $venv_dir/bin/activate
    # run the command
    mpsyt
    # deactivate the venv
    deactivate

else
    echo "Unknown command!"
fi

