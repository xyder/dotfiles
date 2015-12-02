import argparse
from enum import Enum
import json
import os
import sys


def explode(*args):
    return os.path.abspath(os.path.expandvars(os.path.expanduser(os.path.join(*args))))


def load_settings(logger, root_path):
    # prepare settings
    settings = {
        'paths': {
            'settings': os.path.join(root_path, 'data', 'settings.json'),
            'home': os.path.expanduser('~'),
            'dotfiles': root_path[:root_path.rfind('dotfiles') + len('dotfiles')],
            'root': root_path,
            'installers': os.path.join(root_path, 'tools'),
            'log_file': os.path.join(root_path, 'data', 'dpkg.log'),
        },
    }

    # load settings file
    try:
        with open(explode(settings['paths']['settings'])) as settings_file:
            external = json.load(settings_file)
            if 'paths' in external:
                settings['paths'].update(external['paths'])
            external.pop('paths')
            settings.update(external)
    except IOError:
        logger.die_with_msg('Settings file "%s" could not be read! Exiting...' % settings['paths']['settings'])

    return settings


def generic_setup(root_path):
    logger = Logger()
    settings = load_settings(logger, root_path)

    path = explode(settings['paths']['log_file'])
    if os.path.isfile(path):
        os.remove(os.path.abspath(path))

    return logger, settings


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Only simulate actions.')
    args = parser.parse_args()
    return {
        'dry_run': args.dry_run or False
    }

class Logger(object):
    labels = ['I', 'E', 'W', 'F']
    type_names = ['INFO', 'ERROR', 'WARNING', 'FATAL']
    types = Enum('MessageType', ' '.join(type_names))

    def __init__(self, to_console=True, to_file=False):
        self._to_console = to_console
        self._to_file = to_file

    def error(self, *args, show_label=True, **kwargs):
        self.msg(*args, message_type=self.types.ERROR, show_label=show_label, file=sys.stderr, **kwargs)

    def info(self, *args, show_label=True, **kwargs):
        self.msg(*args, message_type=self.types.INFO, show_label=show_label, **kwargs)

    def warning(self, *args, show_label=True, **kwargs):
        self.msg(*args, message_type=self.types.WARNING, show_label=show_label, **kwargs)

    def empty(self):
        self.msg(show_label=False)

    def die_with_msg(self, *args, exit_code=1, **kwargs):
        self.error(*args, **kwargs)
        sys.exit(exit_code)

    def die_for_sudo(self):
        if os.getuid() != 0:
            self.die_with_msg('Must be root to run this section.')

    def msg(self, *args, message_type=types.INFO, show_label=True, **kwargs):
        args = list(args)
        if show_label and len(args):
            if isinstance(args[0], str):
                args[0] = '[%s] ' % self.labels[message_type.value - 1] + args[0]

        if self._to_console:
            print(*args, **kwargs)

        if self._to_file:
            raise NotImplementedError('Logging to file is not implemented yet.')


class ConsoleCursor(object):
    """
    Note: This may not work in all terminals.
    """

    _PREV_LINE = '\033[F'
    _CLEAR_CURRENT = '\033[K'
    _LINE_START = '\033[100D'  # move 100 columns backwards

    @staticmethod
    def prev_line():
        print(ConsoleCursor._PREV_LINE, end='')
        ConsoleCursor.line_start()

    @staticmethod
    def clear_line():
        print(ConsoleCursor._CLEAR_CURRENT, end='')
        ConsoleCursor.line_start()

    @staticmethod
    def line_start():
        print(ConsoleCursor._LINE_START, end='')


def get_progress_bar(length, percentage):
    filled = int(abs(length/100 * percentage))
    empty = length - filled
    return '\u2588' * filled + '\u2591' * empty
