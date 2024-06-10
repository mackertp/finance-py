#!/bin/bash
: '
Simple script based off of the littlest JupyterHub.
https://tljh.jupyter.org/en/latest/install/custom-server.html

@author Preston Mackert
'

# General Linux Setup - update package index cache and packages
apt-get update 
apt-get upgrade -y
apt-get install -y bzip2 gcc git htop screen vim wget  # system tools
apt-get upgrade -y bash
sudo apt install python3 python3-dev git curl
apt-get clean

# Install the littlest jupyterhub and create the admin user
curl -L https://tljh.jupyter.org/bootstrap.py | sudo -E python3 - --admin p.mackert
