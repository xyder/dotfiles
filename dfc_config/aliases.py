import shutil


from .common import activate_ssh_agent


_apt_cmd = 'sudo apt-get'
_cache_cmd = 'apt-cache'


# format: (command, alias, description) or dict
aliases = dict(
    cds=('cd $(find ${1:-.} -type d | fzf)', '', 'Search sub-directories and jump to them'),
    sudo=('sudo', '_', ''),
    dea=('direnv allow ${@:-.}', '', 'reload direnv for current directory'),
    original=('command', '', 'run original commands that were overwritten by aliases'),
    e=('nvim', '', 'edit with nvim'),
    vim=('nvim', '', 'edit with nvim'),
    clr=('echo -en "\ec"', '', 'clear screen'),
    g=('git', '', ''),
    q=('exit', '', ''),
    dsz=('du -h --max-depth=1 . | sort -rh', '', 'list directories and their sizes from the current directory'),
    zreload=('source ~/.zshrc', '', 'reload zsh config'),

    # dfc aliases
    dc_list=('dc list', 'l!', 'list local commands'),
    dc_search=('dc_search', 's!', 'search local commands'),
    dc_search_target=('dc_search_target', 'st!', 'search local commands and return target'),
    dc_run=('dc_run', 'r!', 'run local command'),

    dc_list_global=('dc -g list', 'l.!', 'list all commands'),
    dc_search_global=('dc_search_global', 's.!', 'search all commands'),
    dc_search_target_global=('dc_search_target_global', 'st.!', 'search all commands and return target'),
    dc_run_global=('dc_run_global', 'r.!', 'run any command'),

    # apt aliases
    apti=(f'{_apt_cmd} install', '', 'apt install'),
    aptr=(f'{_apt_cmd} remove', '', 'apt remove'),
    aptp=(f'{_apt_cmd} purge', '', 'apt purge'),
    aptc=(f'{_apt_cmd} clean', '', 'apt clean'),
    aptu=(f'{_apt_cmd} update', '', 'apt update'),
    aptU=(f'{_apt_cmd} update && {_apt_cmd} upgrade', '', 'apt upgrade'),

    # apt cache aliases
    apts=(f'{_cache_cmd} search', '', 'apt search'),
    aptsn=(f'{_cache_cmd} search --names-only', '', 'apt search names'),
    aptl=(f'{_cache_cmd} pkgnames', '', 'list packages. can also search with it.'),
    aptinfo=(f'{_cache_cmd} show', '', 'show info for package'),
    aptdep=(f'{_cache_cmd} showpkg', '', 'check package dependencies'),
    aptstat=(f'{_cache_cmd} stats', '', 'apt stats'),

    gg=('git gui &', '', 'run git gui in background'),

    ls=('ls', '', 'list files'),
    la=('ls -la', '', 'list all, in a list'),
    ll=('ls -a', '', 'list all'),

    # ssh aliases
    ssha=(activate_ssh_agent, '', 'start ssh agent'),
    sshl=('ssh-add -l', '', 'list loaded keys'),

    # pip aliases
    pip=('pip3', '', ''),
    # docker commands
    dk=('docker', '', 'docker'),
    dkb=('docker build', '', 'docker build'),

    dk_i_dang=('docker images -f "dangling=true"', '', 'list dangling images'),
    dk_rmi_dang=('docker rmi $(docker images -f "dangling=true" -q)', '', 'remove dangling images'),
    dk_i_ls=('docker images ls -a', '', 'list all images'),

    dk_l=('docker logs -tf --tail', '', 'tail logs for a container'),

    dkc=('docker-compose', '', ''),
    dkc_u=('docker-compose up -d', '', 'docker-compose up dettached'),

    # create up movers dynamically
    **{
        f'cd{i}': (f'cd {"/".join(i * [".."])}', (i + 1) * '.', f'Go up {i} level(s)')
        for i in range(1, 6)
    }
)

# change aliases to use exa if available
if shutil.which('exa'):
    aliases.update(dict(
        ls=('exa -G  --color auto --icons -a -s type', '', 'list, standard'),
        ll=('exa -l --color always --icons -a -s type', '', 'list, long'),
        la=('exa -lGa --color always --icons -a -s type', '', 'list, all'),
    ))
