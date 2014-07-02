#!/usr/bin/python3

import argparse
import sys

from usersync import config, lp, sync

PROVIDERS = {
    'lp': lp,
}


def _configured_users(args, cfg):
    provider = PROVIDERS[args.provider]
    users = {}
    for team in cfg.get('team', []):
        users.update(provider.get_people(team))
    for user in cfg.get('users', []):
        users.update({user: provider.get_ssh_keys(user)})
    return users


def _get_args():
    parser = argparse.ArgumentParser(
        description='''Syncronize user accounts defined somewhere like
                    like launchpad.net into a local group. Much easier to use
                    and administer than something like ldap''')
    parser.add_argument('--provider', default='lp',
                        choices=PROVIDERS.keys(),
                        help='Team/sshkey provider. default=%(default)s')
    parser.add_argument('--config', default=config.DEFAULT,
                        help='Config file to use. default=%(default)s')
    parser.add_argument('--backupdir', default='/root/disabled-users',
                        help='''Directory to back up deleted user\'s home
                             directories to. default=%(default)s''')
    parser.add_argument('--dryrun', action='store_true',
                        help='Make no changes, just display actions')
    return parser.parse_args()


def main():
    args = _get_args()

    sync.DRY_RUN = args.dryrun
    cfg = config.load(args.config)

    group = cfg.get('local_group', ['users'])[0]
    local = sync.get_local_users(group)
    users = _configured_users(args, cfg)

    sync.delete_users(local, users, args.backupdir)
    sync.add_users(local, users, group)
    sync.update_users(local, users)

    #TODO sudo


if __name__ == '__main__':
    sys.exit(main())
