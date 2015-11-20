#!/usr/bin/env python2.7
import json
import os.path
import uuid

from fabric.api import *

env.user = 'vagrant'
env.hosts = ['127.0.0.1:2222']
env.key_filename = './.vagrant/machines/default/virtualbox/private_key'


def decrypt(filename, password):
    '''Uses pkware to decrypt `filename` into a unique directory'''
    vagrantdir = os.path.dirname(__file__)
    id = uuid.uuid1()
    workdir = '{vagrantdir}/tmp/{id}'.format(vagrantdir=vagrantdir, id=id)
    local('mkdir {workdir}'.format(workdir=workdir))
    local('cp {filename} {workdir}'.format(filename=filename, workdir=workdir))
    basename = os.path.basename(filename)
    run('''\
    pkzipc -extract -passphrase="{password}" \
      /vagrant/tmp/{id}/{basename} \
      /vagrant/tmp/{id}
    '''.format(password=password, id=id, basename=basename))
    print 'Decrypted into {workdir}'.format(workdir=workdir)
