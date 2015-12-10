import os
import apt
from .utils import get_progress_bar, Logger, ConsoleCursor as cc


class CustomAcquireProgress(apt.progress.base.AcquireProgress):
    pass


class CustomInstallProgress(apt.progress.base.InstallProgress):
    _first_state_change = True

    def __init__(self, log_file=None, logger=None, *args, **kwargs):
        self._logger = logger or Logger()
        self.log_file = log_file
        super().__init__(*args, **kwargs)

    def fork(self):
        # Note: might require override of conffile() and error() too
        pid = os.fork()

        if self.log_file:
            if pid == 0:
                # reroute stdout and stderr into a file
                logfd = os.open(self.log_file, os.O_RDWR | os.O_APPEND | os.O_CREAT, 0o644)
                os.dup2(logfd, 1)
                os.dup2(logfd, 2)
        return pid

    def status_change(self, pkg, percent, status):
        if self._first_state_change:
            self._first_state_change = False
        else:
            cc.clear_line()

        self._logger.info('%s [%s]' % (get_progress_bar(30, percent), pkg), end='\r')

    @staticmethod
    def finish_update():
        cc.clear_line()


class AptManager(object):

    def __init__(self, logger, log_file=None):
        self._logger = logger
        self._log_file = log_file
        self._cache = apt.Cache()

    @staticmethod
    def reload_cache(cache):
        cache.update()

        # re-open to use the new cache
        cache.open(None)

    def install_packages(self, packages, dry_run=False):
        marked_packages = []
        for package in packages:
            if package in self._cache:
                pkg = self._cache[package]
            else:
                self._logger.error('Package "%s" not found.' % package)
                continue

            if pkg.is_installed:
                self._logger.info('Package "%s" is already installed.' % package)
            else:
                marked_packages.append(package)
                if not dry_run:
                    pkg.mark_install()

        cip = CustomInstallProgress(log_file=self._log_file, logger=self._logger)
        try:
            self._cache.commit(CustomAcquireProgress(), cip)
        except Exception as e:
            self._logger.error('Packages "%s" failed to install: %s' % (', '.join(marked_packages), e))
            return

        for package in marked_packages:
            self._logger.info('Package "%s" successfully installed.' % package)
