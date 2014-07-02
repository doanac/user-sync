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
    url = 'https://api.github.com/users/%s/keys' % user
    resp = _get(url)
    return [x['key'] for x in resp]


def get_people(team):
    # TODO figure this out
    # grab something like https://api.github.com/orgs/<org>/teams/
    raise NotImplementedError()
