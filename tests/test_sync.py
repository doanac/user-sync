#!/usr/bin/python3

import unittest
from unittest import mock

from usersync import sync


class TestConfig(unittest.TestCase):
    @mock.patch('pwd.getpwall')
    @mock.patch('grp.getgrnam')
    def test_local_users(self, grnam, pwall):
        grnam().gr_gid = 123
        pwall.return_value = [
            mock.Mock(pw_name='user1', pw_gid=123),
            mock.Mock(pw_name='user2', pw_gid=123),
            mock.Mock(pw_name='user3', pw_gid=124),
        ]
        self.assertEqual(['user1', 'user2'], sync.get_local_users('groupname'))

    @mock.patch('grp.getgrnam')
    def test_local_sudoers(self, grnam):
        grnam().gr_mem = ['u2', 'u4', 'u5']
        users = ['u1', 'u2', 'u3', 'u4']
        self.assertEqual(['u2', 'u4'], sync.get_local_sudoers(users))

    @mock.patch('usersync.sync._delete')
    def test_delete_users(self, delete):
        local = ['u1', 'u2', 'u3']
        remote = {'u1': 'foo', 'u3': 'foo'}
        sync.delete_users(local, remote, None)
        delete.assert_called_once_with('u2', None)

    @mock.patch('usersync.sync._add')
    @mock.patch('grp.getgrnam')
    def test_add_users(self, grnam, add):
        grnam().gr_gid = 123
        local = ['u1', 'u2', 'u3']
        remote = {'u1': 'foo', 'u3': 'foo', 'u4': 'blah'}
        sync.add_users(local, remote, 'grpname')
        add.assert_called_once_with('u4', 'blah', 123)
