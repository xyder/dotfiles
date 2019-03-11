#!/usr/bin/env zsh


die() {
    printf '%s\n' "$1" >&2
    exit 1
}


msg() {
    printf '-- %s\n' "$1"
}


show_help() {
cat << EOF
Usage: ${0##*/} [-h|--help] [-v|--venv VENV_DIR] [-e|--env ENV_FILE] -- CMD
Activate VENV_DIR/bin/activate, load ENV_FILE and run CMD.

    -h|--help           display this help and exit
    -v|--venv VENV_DIR  activate VENV_DIR/bin/activate before running CMD. If not specified, ./venv will be used if exists
    -e|--env ENV_FILE   load ENV_FILE. If not specified, ./.env will be used if exists
EOF
}

DEFAULT_ENV=.env
DEFAULT_VENV=venv/bin/activate

cmd=
venv_bin=
env_file=


# TODO: should work for both pipenv and venv
while :; do
    case $1 in
        -h|--help)
            show_help
            exit
            ;;
        -v|--venv)
            if [ "$2" ] && [ -d "$2" ] && [ -f "$2/bin/activate" ]; then
                venv_bin="$2/bin/activate"
                shift
            fi
            ;;
        -e|--env)
            if [ "$2" ] && [ -f "$2" ]; then
                env_file="$2"
                shift
            fi
            ;;
        --)              # End of all options.
            shift
            cmd="$@"
            shift
            break
            ;;
        -?*)
            printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
            ;;
        *)               # Default case: No more options, so break out of the loop.
            break
    esac

    shift
done

# ### process venv
# set venv to default if possible
if [ ! "$venv_bin" ] && [ -f "$DEFAULT_VENV" ]; then
    venv_bin=$DEFAULT_VENV
fi

# activate venv
if [ "$venv_bin" ]; then
    msg "Activating venv: $venv_bin"
    source $venv_bin
fi

# ### process env
# set env to default if possible
if [ ! "$env_file" ] && [ -f "$DEFAULT_ENV" ]; then
    env_file=$DEFAULT_ENV
fi

# load env
if [ "$env_file" ]; then
    msg "Using env: $env_file"
    export `cat $env_file`
fi

# ### run command
printf "\n"
msg "Running: '$cmd'"
printf "\n"

eval $cmd

