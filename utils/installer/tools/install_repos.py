#!/usr/bin/env python3.5
from libs.git_wrapper import GitManager
from libs.utils import generic_setup, parse_args


def clone_repos():
    pass


def main():
    args = parse_args(required_root_path=True)

    logger, settings = generic_setup(args['root_path'])

    clone_repos()

    # GitManager.clone_repo('xyder', 'dotfiles', os.path.expanduser('~/test'))


if __name__ == '__main__':
    main()
