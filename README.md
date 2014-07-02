user-sync
---------

This originated from code written to manage user accounts at Linaro:

 https://code.launchpad.net/~doanac/+junk/linaro-its-tools

Its been cleaned up significantly, but the same idea remains. You create a
config file:
```
  #/etc/user-sync.conf
  users: user1 user2
  team: team1
  # group is optional but will be the local group the users are members of
  group: users
```

The script will then figure out all the users that should be configured locally
based on the user list as well as what users are members of the given team.
It will then grab the ssh keys for those users and make sure there are local
accounts for each user with a proper .authorized_keys file for each user.

The script handles updated sshkeys when needed as well as removing users that
are no longer in a team or listed as a user.

This program currently uses Launchpad teams/sshkeys, but should be able to
support github or any other service similar to this.

This can then be used as a cron job to keep users up-to-date without having
to bother setting up an LDAP server.
