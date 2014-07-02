import os
import re
import sys

DEFAULT = '/etc/user-sync.conf'


def load(config=DEFAULT):
    if not os.path.exists(config):
        sys.exit('Missing config file: %s' % config)

    cfg = {}
    with open(config) as f:
        for line in f.readlines():
            match = re.match(r'(\w+)\s*:\s*(\w+.*$)', line)
            if match:
                vals = [x.strip() for x in match.group(2).split(',')]
                cfg[match.group(1)] = vals
    return cfg
