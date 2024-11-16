#!/bin/bash

: '
Script used to install Linux system tools
and basic Python components.

@author Preston Mackert
'

# General Linux, update package index cache and packages
apt-get update
apt-get upgrade -y

# install system tooling
apt-get install -y bzip2 gcc git htop screen vim wget
apt-get upgrade -y bash
apt-get clean

# install miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O miniconda.sh
bash miniconda.sh -b
rm -rf miniconda.sh
export PATH="root/miniconda3/bin:$PATH"

# update python and install libraries
conda update -y conda python
conda install -y pandas
conda install -y ipython