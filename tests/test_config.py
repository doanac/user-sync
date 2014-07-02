#!/usr/bin/python3

import os
import tempfile
import unittest

from usersync import config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.tmpfile = tempfile.mkstemp()[1]
        self.addCleanup(os.unlink, self.tmpfile)

    def test_no_config(self):
        self.assertRaises(SystemExit, config.load, '/no such file')

    def test_config_1(self):
        with open(self.tmpfile, 'w') as f:
            f.write('users:1,2')
        cfg = config.load(self.tmpfile)
        self.assertEqual({'users': ['1', '2']}, cfg)

    def test_config_2(self):
        with open(self.tmpfile, 'w') as f:
            f.write('users : 1,2\n')
        cfg = config.load(self.tmpfile)
        self.assertEqual({'users': ['1', '2']}, cfg)

    def test_config_3(self):
        with open(self.tmpfile, 'w') as f:
            f.write('#users: 1\n')
            f.write('users : 1, 2 ')
        cfg = config.load(self.tmpfile)
        self.assertEqual({'users': ['1', '2']}, cfg)

    def test_config_4(self):
        with open(self.tmpfile, 'w') as f:
            f.write('users : 1')
        cfg = config.load(self.tmpfile)
        self.assertEqual({'users': ['1']}, cfg)

    def test_config_5(self):
        with open(self.tmpfile, 'w') as f:
            f.write('users:\t1,\t2')
        cfg = config.load(self.tmpfile)
        self.assertEqual({'users': ['1', '2']}, cfg)
