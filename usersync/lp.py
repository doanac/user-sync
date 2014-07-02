import json
import urllib.request


def _get(url):
    resp = urllib.request.urlopen(url)
    resp = resp.read().decode('utf8')
    return json.loads(resp)


def _collection(url):
    '''iterate through each item returned in an lp_collection'''
    data = _get(url)

    for d in data['entries']:
        yield d

    if 'next_collection_link' in data:
        for d in _collection(data['next_collection_link']):
            yield d


def get_ssh_keys(user):
    url = 'https://launchpad.net/~%s/+sshkeys' % user
    resp = urllib.request.urlopen(url)
    return resp.read().decode('utf8')


def get_people(team):
    url = 'https://api.launchpad.net/1.0/~%s/members' % team
    users = {}
    for entry in _collection(url):
        name = entry['name']
        if entry['is_team']:
            users.update(get_people(name))
        elif name not in users:
            users[name] = get_ssh_keys(name)
    return users
