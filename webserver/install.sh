#!/usr/bin/env bash
set -euo pipefail

### Get directory where this script is installed
BASEDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
RELEASE_FILE="$HOME/mini-pupper-release"

if [ ! -f /etc/os-release ]; then
    echo "Cannot detect OS version (/etc/os-release missing)."
    exit 1
fi

source /etc/os-release
if [[ "${UBUNTU_CODENAME:-}" != "jammy" && "${UBUNTU_CODENAME:-}" != "noble" ]]; then
    echo "Ubuntu 22.04 (jammy) or 24.04 (noble) is required. Current: ${VERSION:-unknown}"
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is required. Install it first."
    exit 1
fi

if ! python3 -m pip --version >/dev/null 2>&1; then
    echo "python3-pip not found, installing it..."
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

PIP_FLAGS=()
if [[ "${UBUNTU_CODENAME:-}" == "noble" ]]; then
    PIP_FLAGS=(--break-system-packages)
fi

update_release_key() {
    local key="$1"
    local value="$2"
    if grep -q "^${key}=" "$RELEASE_FILE"; then
        sed -i "s|^${key}=.*|${key}=\"${value}\"|" "$RELEASE_FILE"
    else
        echo "${key}=\"${value}\"" >> "$RELEASE_FILE"
    fi
}

pip_install() {
    if sudo -H python3 -m pip install "${PIP_FLAGS[@]}" "$@"; then
        return 0
    fi
    # Fallback for environments that enforce stricter package policies.
    sudo -H python3 -m pip install --break-system-packages "$@"
}

pip_install_with_pbr() {
    local version="$1"
    shift
    if sudo -H PBR_VERSION="$version" python3 -m pip install "${PIP_FLAGS[@]}" "$@"; then
        return 0
    fi
    sudo -H PBR_VERSION="$version" python3 -m pip install --break-system-packages "$@"
}

touch "$RELEASE_FILE"

if [ -x "$HOME/mini_pupper_bsp/get-version.sh" ]; then
    VERSION=$(cd "$BASEDIR"; "$HOME/mini_pupper_bsp/get-version.sh")
else
    VERSION="0.0.0"
fi

update_release_key "WEBCONTROLLER_VERSION" "$VERSION"

source "$RELEASE_FILE"
IS_RELEASE=${IS_RELEASE:-NO}

sudo rm -rf /usr/lib/python3/dist-packages/blinker*
if [ "$IS_RELEASE" == "YES" ]
then
    cd "$BASEDIR"
    TAG_COMMIT=$(git rev-list --abbrev-commit --tags --max-count=1)
    TAG=$(git describe --abbrev=0 --tags ${TAG_COMMIT} 2>/dev/null || true)
    if [ "v$WEBCONTROLLER_VERSION" != "$TAG" ]
    then
        sed -i "s/IS_RELEASE=YES/IS_RELEASE=NO/" ~/mini-pupper-release
    fi
    pip_install_with_pbr "$VERSION" "$BASEDIR/backend"
    pip_install_with_pbr "$VERSION" "$BASEDIR/../joystick_sim"
else
    pip_install "$BASEDIR/backend"
    pip_install "$BASEDIR/../joystick_sim"
fi

sudo install -m 0644 "$BASEDIR/web-controller.service" /etc/systemd/system/web-controller.service
sudo systemctl daemon-reload
sudo systemctl enable web-controller
sudo systemctl restart web-controller
