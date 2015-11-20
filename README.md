# pkware-vagrant
Runs PKWARE in Vagrant.  Useful to use PKWARE on a Mac.

Initial setup:
```
# virtual environment
$ virtualenv env
$ source env/bin/activate
$ pip install -r ./requirements.txt

# vagrant
$ cp <path to pkware rpm> ./  # `vagrant up` will install the pkware rpm
$ vagrant up
$ vagrant ssh
```

Encrypt a file:
```
vagrant$ pkzipc -add -passphrase=<p> <path-to-zip> <paths to add to zip> ...
```

Decrypt a file:
```
local$ fab decrypt:<filename>,<password>
```
