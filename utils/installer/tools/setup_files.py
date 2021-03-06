#!/usr/bin/env python3.5

import os
import shutil
import errno
from libs.utils import generic_setup, explode, parse_args


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


def create_backups(logger, settings, dry_run=False):
    logger.empty()
    logger.info('Backing up some files if necessary..')

    for backup in settings['backups']:
        src = explode(*backup)
        # only backup if source file exists and is not a symlink already
        if os.path.exists(src) and not os.path.islink(src) and os.path.isfile(src):
            logger.info('Backing up "%s".' % src)
            if not dry_run:
                shutil.copy2(src, os.path.abspath(src) + '.xbkp')


def create_symlinks(logger, settings, path=None, val=None, dry_run=False):
    if 'tag_run_once' not in dir(create_symlinks):
        logger.empty()
        logger.info('Creating symlinks..')
        create_symlinks.tag_run_once = True

    if not path:
        path = explode(settings['paths']['dotfiles'])

    if not val:
        val = settings['paths']['symlinks']

    if isinstance(val, dict):
        for k, v in val.items():
            create_symlinks(logger, settings, explode(path, k), v, dry_run=dry_run)
    else:
        if dry_run:
            logger.info('%s -> %s' % (explode(*val), path))
        else:
            os.makedirs(explode(*val[:-1]), exist_ok=True)
            symlink(logger, path, explode(*val), forced=True)


def main():
    args = parse_args(required_root_path=True)

    logger, settings = generic_setup(args['root_path'])

    create_backups(logger, settings, dry_run=args['dry_run'])
    create_symlinks(logger, settings, dry_run=args['dry_run'])


if __name__ == '__main__':
    main()
