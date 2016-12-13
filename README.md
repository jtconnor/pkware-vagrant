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
$ cp <path to pkware rpm> ./  # Download PKWARE rpm from their website
$ vagrant up  # Installs the pkware rpm
```

Encrypt a file or directory
```
$ fab encrypt:<file-or-directory>,<password>
```

Decrypt a file
```
$ fab decrypt:<file>,<password>
```
