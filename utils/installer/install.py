#!/usr/bin/env python3.5
from functools import partial

import os
import shutil
import sys
import subprocess
import pip
from tools.libs.utils import generic_setup, explode, parse_args, get_script_path


def call_command(path, args=[], sudo=False, die_on_error=True):
    args = ['sudo'] * sudo + [path] + args
    return_code = subprocess.call(args)

    if die_on_error and return_code != 0:
        sys.exit(1)


def call_install_script(script_file, settings, args=[], sudo=False, die_on_error=True):
    call_command(explode(settings['paths']['installers'], script_file), args=args, sudo=sudo, die_on_error=die_on_error)


def main():
    args = parse_args()

    if not args['root_path']:
        root_path = os.path.dirname(os.path.realpath(__file__))
    else:
        root_path = args['root_path']

    logger, settings = generic_setup(root_path)

    cmd_args = []
    dry_run = False
    if args['dry_run']:
        cmd_args += ['--dry-run']
        dry_run = True
    cmd_args += ['--root-path', root_path]

    gsp = partial(get_script_path, settings)

    call_install_script(gsp('apps'), settings, args=cmd_args, sudo=True)
    pip.main(['install', 'gitpython'])
    call_install_script(gsp('files'), settings, args=cmd_args)
    call_install_script(gsp('repos'), settings, args=cmd_args)

    call_command(explode('~/tmp-fonts/install.sh'))
    shutil.rmtree(explode('~/tmp-fonts'))
    call_command('vim', args=['+PluginInstall', '+qall'])


if __name__ == '__main__':
    main()
