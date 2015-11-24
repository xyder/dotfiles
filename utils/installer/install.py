#!/usr/bin/env python3
import os
import errno
import json
import sys
import argparse
import subprocess
import shutil
from libs import AptManager
from libs.utils import Logger


def load_settings(logger):
    # prepare settings
    my_path = os.path.dirname(os.path.realpath(__file__))
    settings = {
        'path.settings': os.path.join(my_path, 'settings.json'),
        'path.home': os.path.expanduser('~'),
        'path.dotfiles': my_path[:my_path.rfind('dotfiles') + len('dotfiles')],
        'path.installer': my_path,
        'path.log_file': os.path.join(my_path, 'dpkg.log'),
        'app.sections': {
            'core': install_core_apps
        }
    }

    # load settings file
    try:
        with open(settings['path.settings']) as settings_file:
            settings.update(json.load(settings_file))
    except IOError:
        logger.die_with_msg('Settings file "%s" could not be read! Exiting...' % settings['path.settings'])

    return settings


def symlink(logger, target, link_path, target_is_directory=False, forced=True):
    try:
        os.symlink(target, link_path, target_is_directory=target_is_directory)
        logger.info('Created symlink: "%s"' % link_path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            if forced:
                logger.warning('Overwriting symlink: "%s"' % link_path)
                if os.path.isdir(link_path) and not os.path.islink(link_path):
                    os.removedirs(link_path)
                else:
                    os.remove(link_path)
                os.symlink(target, link_path, target_is_directory=target_is_directory)
            else:
                logger.error('Symlink "%s" already exists.' % link_path)
        else:
            logger.die_with_msg('[OSError] %s. Exiting... ' % e.strerror)


def create_symlinks(logger, settings, path=None, val=None, dry_run=False):
    if not path:
        path = settings['path.dotfiles']

    if not val:
        val = settings['path.symlinks']

    if isinstance(val, dict):
        for k, v in val.items():
            create_symlinks(logger, settings, os.path.join(path, k), v, dry_run=dry_run)
    else:
        if dry_run:
            logger.info('%s -> %s' % (os.path.join(settings['path.home'], *val), path))
        else:
            os.makedirs(os.path.join(settings['path.home'], *val[:-1]), exist_ok=True)
            symlink(logger, path, os.path.join(settings['path.home'], *val), forced=True)


def install_core_apps(settings, logger):
    logger.info('Section "core": Installing applications..')
    logger.die_for_sudo()

    am = AptManager(logger, log_file=settings['path.log_file'])

    logger.info('Installing packages: %s.' % ', '.join(settings['packages.core']))
    am.install_packages(settings['packages.core'])


def backup_file(src, dest):
    if os.path.exists(src) and not os.path.islink(src) and os.path.isfile(src):
        shutil.copy2(src, dest)


def parse_command_line():
    pass


def main():
    logger = Logger()
    settings = load_settings(logger)

    if os.path.isfile(settings['path.log_file']):
        os.remove(settings['path.log_file'])

    sections = settings['app.sections']

    # parse arguments
    parser = argparse.ArgumentParser(description='Installer for the dotfiles.')
    parser.add_argument('--solo-section', help='runs only this section')
    args = parser.parse_args()

    section = args.solo_section
    if section:
        if section in sections:
            # run the specified section
            sections[section](settings, logger)
        else:
            logger.die_with_msg('Section "%s" not found.' % section)
    else:
        # normal execution
        pass
        returncode = subprocess.call(['sudo'] + sys.argv + ['--solo-section', 'core'])
        if returncode != 0:
            sys.exit(1)

        logger.empty()
        logger.info('Backing up some files if necessary..')
        backup_file(os.path.join(settings['path.home'], '.bashrc'),
                    os.path.join(settings['path.home'], '.bashrc.alt'))

        backup_file(os.path.join(settings['path.home'], '.bash_profile'),
                    os.path.join(settings['path.home'], '.bash_profile.alt'))

        logger.empty()
        logger.info('Creating symlinks..')
        create_symlinks(logger, settings)


if __name__ == '__main__':
    main()
