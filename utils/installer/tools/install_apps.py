#!/usr/bin/env python3.5

from libs import AptManager
from libs.utils import generic_setup, explode, parse_args


def install_apps(logger, settings, dry_run=False):
    logger.info('Section "core": Installing applications..')
    logger.die_for_sudo()

    am = AptManager(logger, log_file=explode(settings['paths']['log_file']))

    logger.info('Installing packages: %s.' % ', '.join(settings['packages']['core']))
    am.install_packages(settings['packages']['core'], dry_run=dry_run)


def main():
    args = parse_args(required_root_path=True)

    logger, settings = generic_setup(args['root_path'])

    install_apps(logger, settings, dry_run=args['dry_run'])

if __name__ == '__main__':
    main()
