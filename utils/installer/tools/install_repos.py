#!/usr/bin/env python3.5
from libs.git_wrapper import GitManager
from libs.utils import generic_setup, parse_args, explode


def clone_repos(logger, settings, dry_run=False):
    for repo in settings["repositories"]:
        protocol = repo[0]
        host = repo[1]
        user = repo[2]
        repository = repo[3]
        destination = explode(*repo[4])

        logger.info('Cloning repo "%s" into "%s".' % (
            GitManager.get_github_path(
                user=user,
                repo=repository,
                host=host,
                protocol=protocol),
            destination))

        if not dry_run:
            GitManager.clone_repo(user=user,
                                  repository=repository,
                                  destination=destination,
                                  protocol=protocol,
                                  host=host)


def main():
    args = parse_args(required_root_path=True)

    logger, settings = generic_setup(args['root_path'])

    clone_repos(logger, settings, dry_run=args['dry_run'])


if __name__ == '__main__':
    main()
