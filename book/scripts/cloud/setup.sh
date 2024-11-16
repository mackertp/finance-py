#!/bin/bash
: '
Setting up a DigitalOcean Droplet with 
basic Python stack and Jupyter

@author Preston Mackert
'

# IP address from executed command
MASTER_IP=$1

# copy bash scripts to the droplet
scp install.sh root@${MASTER_IP}:

# Execute the install script
ssh root@${MASTER_IP} bash /root/install.sh