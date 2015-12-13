import shutil
from git import Repo
import os
from libs.utils import Logger


class GitManager(object):
    DEFAULT_HOST = 'github.com'
    DEFAULT_PROTOCOL = 'git'

    def __init__(self, logger=None):
        self._loger = logger or Logger()

    @staticmethod
    def get_github_path(user, repo, host=DEFAULT_HOST, protocol=DEFAULT_PROTOCOL):
        if user and repo:
            ending = '%s/%s.git' % (user, repo)
            if protocol == 'ssh':
                return 'git@%s:%s' % (host, ending)

            if protocol == 'git' or protocol == 'https':
                return '%s://%s/%s' % (protocol, host, ending)
        return ''

    @staticmethod
    def get_bitbucket_path(user, repo, ssh=True):
        # TODO: Implement a bitbucket url build function.
        raise NotImplementedError()

    @staticmethod
    def clone_repo(user, repository, destination, protocol=DEFAULT_PROTOCOL, host=DEFAULT_HOST, forced=True):
        if os.path.islink(destination) or os.path.exists(destination):
            if not forced:
                raise Exception('Path "%s" already exists.' % destination)

            if os.path.isdir(destination) and not os.path.islink(destination):
                shutil.rmtree(destination)
            else:
                os.remove(destination)

        os.makedirs(destination, exist_ok=True)

        Repo.clone_from(GitManager.get_github_path(user, repository, host, protocol), destination, ssh=False)
