#!/usr/bin/bash
set -x

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

source  ~/mini-pupper-release

### Append to release file
echo WEBCONTROLLER_VERSION=\"$(cd $BASEDIR; ~/mini_pupper_bsp/get-version.sh)\" >> ~/mini-pupper-release

sudo rm -rf /usr/lib/python3/dist-packages/blinker*
if [ "$IS_RELEASE" == "YES" ]
then
    sudo PBR_VERSION=$(cd $BASEDIR; ~/mini_pupper_bsp/get-version.sh)  pip install $BASEDIR/backend
    sudo PBR_VERSION=$(cd $BASEDIR; ~/mini_pupper_bsp/get-version.sh)  pip install $BASEDIR/../joystick_sim
else:
    sudo pip install $BASEDIR/backend
    sudo pip install $BASEDIR/../joystick_sim
fi

sudo ln -s $BASEDIR/web-controller.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable web-controller
sudo systemctl start web-controller
