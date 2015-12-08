#!/usr/bin/env python3.5
from functools import partial

import os
import sys
import subprocess
from tools.libs.utils import generic_setup, explode, parse_args, locate_path, get_script_path


def call_script(path, args=[], sudo=False, die_on_error=True):
    args = ['sudo'] * sudo + [path] + args
    return_code = subprocess.call(args)

    if die_on_error and return_code != 0:
        sys.exit(1)


def call_install_script(script_file, settings, args=[], sudo=False, die_on_error=True):
    call_script(explode(settings['paths']['installers'], script_file), args=args, sudo=sudo, die_on_error=die_on_error)


def main():
    args = parse_args()
    cmd_args = []
    if args['dry_run']:
        cmd_args += ['--dry-run']
    my_path = os.path.dirname(os.path.realpath(__file__))
    logger, settings = generic_setup(my_path)

    gsp = partial(get_script_path, settings)

    call_install_script(gsp('apps'), settings, args=cmd_args, sudo=True)
    call_install_script(gsp('files'), settings, args=cmd_args)
    call_install_script(gsp('repos'), settings, args=cmd_args)

if __name__ == '__main__':
    main()
