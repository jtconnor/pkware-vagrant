#!/usr/bin/env python2.7
'''Encrypts and decrypts files using pkware in a VM.'''
import datetime
import fabric.api as fab
import os.path
import subprocess


ssh_config = {}
for line in subprocess.check_output(['vagrant', 'ssh-config']).split('\n'):
    line = line.strip()
    if not line:
        continue
    key, value = line.split(' ')
    ssh_config[key] = value

fab.env.user = ssh_config['User']
fab.env.hosts = ['{}:{}'.format(ssh_config['HostName'], ssh_config['Port'])]
fab.env.key_filename = ssh_config['IdentityFile']


def _create_tmpdirs():
    tmpdir = '~/pkware-vagrant'
    fab.run('rm -rf {}'.format(tmpdir))
    encrypted_dir = tmpdir + '/e'
    fab.run('mkdir -p {}'.format(encrypted_dir))
    decrypted_dir = tmpdir + '/d'
    fab.run('mkdir {}'.format(decrypted_dir))
    return tmpdir, encrypted_dir, decrypted_dir


def encrypt(file_or_directory, password, output_filename=None):
    tmpdir, encrypted_dir, decrypted_dir = _create_tmpdirs()

    if os.path.isdir(file_or_directory):
        fab.put(file_or_directory + '/*', decrypted_dir)
    else:
        fab.put(file_or_directory, decrypted_dir)

    fab.run('''\
    pkzipc -add -passphrase='{password}' \
      {encrypted_dir}/out.zip {decrypted_dir}/*
    '''.format(
        password=password, encrypted_dir=encrypted_dir,
        decrypted_dir=decrypted_dir))

    if output_filename is None:
        dirname = os.path.dirname(file_or_directory)
        basename = os.path.basename(file_or_directory)
        output_filename = os.path.join(
            dirname,
            '{}-encrypted.zip'.format(basename))

    fab.get('{}/out.zip'.format(encrypted_dir), output_filename)
    print 'Encrypted to {}'.format(output_filename)

    fab.run('rm -rf {}'.format(tmpdir))


def decrypt(filename, password, output_dir=None):
    tmpdir, encrypted_dir, decrypted_dir = _create_tmpdirs()

    fab.put(filename, encrypted_dir)

    fab.run('''\
    pkzipc -extract -passphrase='{password}' \
      {encrypted_dir}/* {decrypted_dir}
    '''.format(
        password=password, encrypted_dir=encrypted_dir,
        decrypted_dir=decrypted_dir))

    if output_dir is None:
        dirname = os.path.dirname(filename)
        basename = os.path.basename(filename)
        output_dir = os.path.join(
            dirname,
            '{}-decrypted'.format(basename))
        fab.local('mkdir \'{}\''.format(output_dir))

    fab.get(decrypted_dir + '/*', output_dir)
    print 'Decrypted to {}'.format(output_dir)

    fab.run('rm -rf {}'.format(tmpdir))
