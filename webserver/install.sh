#!/usr/bin/bash
set -x

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

### Append to release file
echo WEBCONTROLLER_VERSION=\"$(cd $BASEDIR; ~/mini_pupper_bsp/get-version.sh)\" >> ~/mini-pupper-release

source  ~/mini-pupper-release

sudo rm -rf /usr/lib/python3/dist-packages/blinker*
if [ "$IS_RELEASE" == "YES" ]
then
    cd $BASEDIR
    TAG_COMMIT=$(git rev-list --abbrev-commit --tags --max-count=1)
    TAG=$(git describe --abbrev=0 --tags ${TAG_COMMIT} 2>/dev/null || true)
    if [ "v$WEBCONTROLLER_VERSION" != "$TAG" ]
    then
        sed -i "s/IS_RELEASE=YES/IS_RELEASE=NO/" ~/mini-pupper-release
    fi
    VERSION=$(cd $BASEDIR; ~/mini_pupper_bsp/get-version.sh)
    sudo PBR_VERSION=$VERSION pip install $BASEDIR/backend
    sudo PBR_VERSION=$VERSION  pip install $BASEDIR/../joystick_sim
else
    sudo pip install $BASEDIR/backend
    sudo pip install $BASEDIR/../joystick_sim
fi

sudo ln -s $BASEDIR/web-controller.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable web-controller
sudo systemctl start web-controller
