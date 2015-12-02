#!/usr/bin/env python3.5
from libs.git_wrapper import GitManager
import os
from libs.utils import generic_setup, parse_args


def main():
    args = parse_args()
    my_path = os.path.dirname(os.path.realpath(__file__))
    # go up one level
    my_path = os.path.dirname(my_path)

    logger, settings = generic_setup(my_path)

    # GitManager.clone_repo('xyder', 'dotfiles', os.path.expanduser('~/test'))


if __name__ == '__main__':
    main()
