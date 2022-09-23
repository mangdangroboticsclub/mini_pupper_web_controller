#!/usr/bin/bash

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo pip uninstall -y backend
sudo rm -rf $BASEDIR/backend/backend.egg-info
sudo rm -rf $BASEDIR/backend/build
sudo PBR_VERSION=1.2.3 pip install $BASEDIR/backend
sudo PBR_VERSION=1.2.3 pip install $BASEDIR/../joystick_sim

sudo ln -s /$BASEDIR/web-controller.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable web-controller
sudo systemctl start web-controller
