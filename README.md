# pkware-vagrant
Runs PKWARE in Vagrant.  Useful to use PKWARE on a Mac.

Init virtual environment
```
$ virtualenv env
$ source env/bin/activate
$ pip install -r ./requirements.txt
```

Init vagrant
```
$ cp <path to pkware rpm> ./  # `vagrant up` will install the pkware rpm
$ vagrant up
$ vagrant ssh
```

Encrypt a file
```
$ fab encrypt:<glob-pattern>,<password>
```

Decrypt a file
```
$ fab decrypt:<filename>,<password>
```
