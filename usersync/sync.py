import crypt
import grp
import os
import pwd
import random
import shutil
import stat
import string
import subprocess

DRY_RUN = True


def get_local_users(group):
    gid = grp.getgrnam(group).gr_gid
    return [x.pw_name for x in pwd.getpwall() if x.pw_gid == gid]


def get_local_sudoers(users):
    lp_sudoers = []
    sudoers = grp.getgrnam('sudo').gr_mem
    for u in users:
        if u in sudoers:
            lp_sudoers.append(u)

    return lp_sudoers


def _delete(user, backupdir):
    print('disabling user account:', user)
    if DRY_RUN:
        return

    # make a backup of the user's home
    u = pwd.getpwnam(user)
    if not os.path.exists(backupdir):
        os.makedirs(backupdir, 0o700)

    bname = os.path.join(backupdir, user)
    root = os.path.dirname(u.pw_dir)
    base = os.path.basename(u.pw_dir)
    shutil.make_archive(bname, 'bztar', root, base)

    subprocess.check_output(["userdel", '-r', user])


def delete_users(local, remote, backupdir):
    for x in set(local) - set(remote.keys()):
        _delete(x, backupdir)


def _add(user, sshkeys, gid):
    print('creating user account:', user)
    if DRY_RUN:
        return

    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    passwd = ''.join(random.choice(chars) for i in range(16))

    # not the most secure way, but good enough for a system that only allows
    # pubkey logins
    epasswd = crypt.crypt(passwd, user)

    subprocess.check_output(
        ['useradd', '-c', 'user-sync managed', '-g', str(gid),
         '-p', epasswd, '-s', '/bin/bash', '-m', user])

    u = pwd.getpwnam(user)
    with open('%s/.password' % u.pw_dir, 'w') as f:
        os.fchmod(f.fileno(), stat.S_IRUSR | stat.S_IWUSR)
        os.fchown(f.fileno(), u.pw_uid, -1)
        f.write('%s' % passwd)
        f.write("\n")


def add_users(local, remote, group):
    gid = grp.getgrnam(group).gr_gid
    for user, keys in remote.items():
        if user not in local:
            _add(user, keys, gid)


def _update(user, sshkeys):
    u = pwd.getpwnam(user)
    sshdir = os.path.join(u.pw_dir, '.ssh')
    keyfile = os.path.join(sshdir, 'authorized_keys')

    if not os.path.exists(sshdir) and not DRY_RUN:
        os.mkdir(sshdir)
        os.chown(sshdir, u.pw_uid, -1)
        os.chmod(sshdir, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

    curkeys = None
    if os.path.exists(keyfile):
        with open(keyfile, 'r') as f:
            curkeys = f.read()

    if curkeys != sshkeys:
        print('updating key for:', user)
        if DRY_RUN:
            return
        with open(keyfile, 'w') as f:
            f.write(sshkeys)
    os.chmod(keyfile, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)
    os.chown(keyfile, u.pw_uid, u.pw_gid)


def update_users(local, users):
    for user, keys in users.items():
        # only need to update for existing users
        if user in local:
            _update(user, keys)
