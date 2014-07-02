#!/usr/bin/python3

import unittest

from unittest import mock

from usersync import lp


class TestLP(unittest.TestCase):
    @mock.patch('usersync.lp._get')
    def test_collection_simple(self, get):
        expected = [1, 2]
        values = {
            'foo': {'entries': expected},
        }
        get.side_effect = lambda x: values[x]
        collection = [x for x in lp._collection('foo')]
        self.assertEqual(expected, collection)

    @mock.patch('usersync.lp._get')
    def test_collection_complex(self, get):
        expected = [1, 2]
        values = {
            'foo': {
                'entries': expected,
                'next_collection_link': 'bar',
            },
            'bar': {
                'entries': expected,
            },
        }
        get.side_effect = lambda x: values[x]
        collection = [x for x in lp._collection('foo')]
        self.assertEqual(expected + expected, collection)

    @mock.patch('usersync.lp.get_ssh_keys')
    @mock.patch('usersync.lp._collection')
    def test_people_simple(self, collection, keys):
        keys.return_value = b'foo'

        expected = {'user1': b'foo', 'user2': b'foo'}
        values = [{'name': x, 'is_team': False} for x in expected.keys()]
        collection.return_value = values

        users = lp.get_people('team')
        self.assertEqual(expected, users)

    @mock.patch('usersync.lp.get_ssh_keys')
    @mock.patch('usersync.lp._collection')
    def test_people_complex(self, collection, keys):
        keys.return_value = b'foo'

        values = {
            'https://api.launchpad.net/1.0/~team/members': [
                {'name': 'user1', 'is_team': False},
                {'name': 'user2', 'is_team': False},
                {'name': 'blahh', 'is_team': True},
            ],
            'https://api.launchpad.net/1.0/~blahh/members': [
                {'name': 'user2', 'is_team': False},
                {'name': 'user3', 'is_team': False},
            ]
        }
        expected = {'user1': b'foo', 'user2': b'foo', 'user3': b'foo'}
        collection.side_effect = lambda x: values[x]

        users = lp.get_people('team')
        self.assertEqual(expected, users)
