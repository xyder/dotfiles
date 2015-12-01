#!/usr/bin/env python3.5

import os
from libs import AptManager
from libs.utils import generic_setup, explode


def install_apps(logger, settings):
    logger.info('Section "core": Installing applications..')
    logger.die_for_sudo()

    am = AptManager(logger, log_file=explode(settings['paths']['log_file']))

    logger.info('Installing packages: %s.' % ', '.join(settings['packages']['core']))
    am.install_packages(settings['packages']['core'])


def main():
    my_path = os.path.dirname(os.path.realpath(__file__))
    # go up one level
    my_path = os.path.dirname(my_path)

    logger, settings = generic_setup(my_path)
    install_apps(logger, settings)

if __name__ == '__main__':
    main()
