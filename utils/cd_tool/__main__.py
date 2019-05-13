#!/usr/bin/env python3

from pathlib import Path

import os
import sys

import argparse
import json
from enum import Enum

WORKING_DIR = Path(__file__).parent.absolute()

CONFIG_PATH = WORKING_DIR / 'ZLF_config.json'


class RegistryException(Exception):
    pass


class Options(Enum):
    ADD = '-a'
    LIST = '-l'
    DELETE = '-d'
    GET = None


class Commands(Enum):
    GOTO = 'cd {}'
    EDIT = 'e {}'
    PRINT = '{}'


class Registry:

    @property
    def entries(self):
        return self._data['entries']

    @entries.setter
    def entries(self, data):
        self._data['entries'] = data

    def __init__(self):
        try:
            with open(CONFIG_PATH, 'r') as file:
                self._data = json.load(file)
        except FileNotFoundError:
            # initialize the data
            self._data = {
                'entries': {},
                'config': {}
            }
            self.write_registry()

        self.options_map = {
            Options.ADD: self.add,
            Options.DELETE: self.delete,
            Options.LIST: self.list,
            Options.GET: self.get
        }

    def write_registry(self):
        with open(CONFIG_PATH, 'w') as file:
            json.dump(self._data, file)

    def get(self, key):
        if not key:
            # pass through
            return os.getcwd()

        key = key[0]
        try:
            return self.entries[key]
        except KeyError:
            # 2nd pass
            for k in self.entries.keys():
                if key.strip().lower() in k.strip().lower():
                    return self.entries[k]

            # pass through
            return str(Path(key).absolute())

    def add(self, key):
        if not key:
            raise RegistryException('A key is required for an entry to be added.')

        path = os.getcwd() if len(key) == 1 else key[1]
        path = str(Path(path).absolute())
        key = key[0]

        if key in self.entries:
            prompt = input(
                f'WARNING: {key} already exists with path: {self.entries[key]}. Do you wish to overwrite? (y/n)')
            prompt = prompt.strip().lower()
            prompt = False if not prompt else prompt[0] == 'y'

            if not prompt:
                raise RegistryException('Cancelled overwrite.')

            print('Overwriting entry.')

        self.entries[key] = path
        self.write_registry()

    def delete(self, key):
        if not key:
            raise RegistryException('A key is required for the delete operation.')

        errors = []
        for k in key:
            try:
                del self.entries[k]
            except KeyError:
                errors.append(f'Key not found: {k}')

        if errors:
            errors = '\n'.join(errors)
            raise RegistryException(errors)

        self.write_registry()

    def list(self, **kwargs):
        del kwargs

        for k, v in self.entries.items():
            print(f'{k:<16} |        {v}')

    def option(self, option, **kwargs):
        return self.options_map[option](**kwargs)


def parse_args(registry: Registry):
    parser = argparse.ArgumentParser(description='CD with bookmarks.')
    parser.add_argument('key', metavar='KEY PATH', nargs='*', help='key and/or path for an entry')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', action='store_true', help='adds a entry')
    group.add_argument('-l', action='store_true', help='lists all entries')
    group.add_argument('-d', action='store_true', help='deletes an entry')

    args = parser.parse_args()
    picked = [x for x in registry.options_map if x.value and getattr(args, x.value.strip('-'))]
    picked = Options.GET if not len(picked) else picked[0]

    kwargs = {'option': picked, 'key': args.key}

    return kwargs


def main():
    reg = Registry()
    args = parse_args(registry=reg)

    try:
        ret = reg.option(**args)
        if ret:
            path = Path(ret)
            if path.is_file():
                return Commands.EDIT.value.format(ret)
            else:
                return Commands.GOTO.value.format(ret)

    except RegistryException as e:
        print(f'ERROR: {" ".join(e.args)}')
        exit(-1)


if __name__ == '__main__':
    sys.stdout.write(main())

