#!/usr/bin/bash
set -x

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo rm -rf /usr/lib/python3/dist-packages/blinker*
sudo pip install $BASEDIR/backend
sudo pip install $BASEDIR/../joystick_sim

sudo ln -s $BASEDIR/web-controller.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable web-controller
sudo systemctl start web-controller
