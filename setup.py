#!/usr/bin/env python3
from setuptools import setup


setup(
    name='user-sync',
    version='1.0',
    author='Andy Doan',
    author_email='doanac@beadoan.com',
    description='''A tool to synchronize local user accounts with SSH keys
                and teams define in launchapd or github''',
    long_description=open('README.rst').read(),
    packages=['usersync'],
    include_package_data=True,
    entry_points={
        'console_scripts': ['user-sync=usersync.main:main'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
    test_suite='tests',
)
