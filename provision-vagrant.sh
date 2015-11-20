#!/bin/bash
# Installs PKWARE SecureZIP on vagrant box.  `vagrant up` should automatically
# run this script on the vagrant box as part of provisioning (controlled by
# config.vm.provision in Vagrantfile).  Should only run this script on the
# vagrant box.

set -eu -o pipefail

echo "Installing PKWARE SecureZIP..."
sudo rpm -ivh /vagrant/pkware-*.rpm
echo "done."
