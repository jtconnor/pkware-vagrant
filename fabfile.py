#!/usr/bin/env python2.7
import os.path
import uuid

from fabric.api import *

env.user = 'vagrant'
env.hosts = ['127.0.0.1:2222']
env.key_filename = './.vagrant/machines/default/virtualbox/private_key'


def create_workdir():
    vagrantdir = os.path.dirname(__file__)
    id = uuid.uuid1()
    workdir = '{vagrantdir}/tmp/{id}'.format(vagrantdir=vagrantdir, id=id)
    local('mkdir -p {workdir}/encrypted'.format(workdir=workdir))
    local('mkdir {workdir}/decrypted'.format(workdir=workdir))
    return workdir, id


def encrypt(glob, password, name='encrypted'):
    workdir, id = create_workdir()
    local('cp {glob} {workdir}/decrypted'.format(
        glob=glob, workdir=workdir))
    run('''\
    pkzipc -add -passphrase="{password}" \
      /vagrant/tmp/{id}/encrypted/{name}.zip \
      /vagrant/tmp/{id}/decrypted/*
    '''.format(password=password, id=id, name=name))
    print 'Encrypted to {workdir}/encrypted/{name}.zip'.format(
        workdir=workdir, name=name)


def decrypt(filename, password):
    '''Uses pkware to decrypt `filename` into a unique directory'''
    workdir, id = create_workdir()
    local('cp {filename} {workdir}/encrypted'.format(
        filename=filename, workdir=workdir))
    basename = os.path.basename(filename)
    run('''\
    pkzipc -extract -passphrase="{password}" \
      /vagrant/tmp/{id}/encrypted/{basename} \
      /vagrant/tmp/{id}/decrypted
    '''.format(password=password, id=id, basename=basename))
    print 'Decrypted into {workdir}/decrypted'.format(workdir=workdir)
