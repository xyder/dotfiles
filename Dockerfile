FROM python:3.8-buster

# todo: perhaps these should be 1000/1000
ENV USR=xyder \
    GRP=xyder \
    HOMEDIR=/home/xyder

RUN groupadd -r $USR && \
    useradd -rmg $GRP $USR

COPY --chown=$USR:$GRP \
    docker_prereqs/system-requirements.txt \
    $HOMEDIR/dotfiles/docker_prereqs/system-requirements.txt

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    # todo: check if needed: apt-utils dialog less iproute2 procps
    #
    # install system packages
    && apt-get -y install --no-install-recommends \
        `cat $HOMEDIR/dotfiles/docker_prereqs/system-requirements.txt` 2>&1 \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

COPY --chown=$USR:$GRP \
    docker_prereqs/install_system.sh \
    $HOMEDIR/dotfiles/docker_prereqs/

RUN $HOMEDIR/dotfiles/docker_prereqs/install_system.sh \
    && rm -fr $HOMEDIR/docker_prereqs

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PYTHONUNBUFFERED=1

USER $USR

COPY --chown=$USR:$GRP . $HOMEDIR/dotfiles

RUN ["/bin/zsh", "-c", "$HOMEDIR/dotfiles/docker_prereqs/install_user.sh"]

WORKDIR $HOMEDIR

# todo: figure out a better entrypoint
# ENTRYPOINT ["/usr/bin/zsh"]
CMD tail -f /dev/null
