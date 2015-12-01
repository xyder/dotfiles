#!/usr/bin/env python3.5

import os
import sys
import subprocess
from tools.libs.utils import generic_setup, explode


def call_script(path, sudo=False, die_on_error=True):
    args = ['sudo'] * sudo + [path]
    return_code = subprocess.call(args)

    if die_on_error and return_code != 0:
        sys.exit(1)


def call_install_script(script_file, settings, sudo=False, die_on_error=True):
    call_script(explode(settings['paths']['installers'], script_file), sudo=sudo, die_on_error=die_on_error)


def main():
    my_path = os.path.dirname(os.path.realpath(__file__))
    logger, settings = generic_setup(my_path)

    call_install_script('install_apps.py', settings, sudo=True)
    call_install_script('setup_files.py', settings)
    call_install_script('install_repos.py', settings)


if __name__ == '__main__':
    main()
