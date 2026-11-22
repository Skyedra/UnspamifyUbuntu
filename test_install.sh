#!/bin/bash
# Install the package over a stock Ubuntu Pro client and check that the tools still start
set -euo pipefail

SRC=$(cd "$(dirname "$0")" && pwd)
DEB=$(realpath "${1:-$SRC/fake-ubuntu-advantage-tools/fake-ubuntu-advantage-tools.deb}")
PRO_PKGS="ubuntu-pro-client ubuntu-advantage-tools ubuntu-advantage-desktop-daemon"
export DEBIAN_FRONTEND=noninteractive

step() { printf '\n=== %s\n' "$*"; }
fail() { echo "FAIL: $*" >&2; exit 1; }
installed() { [ "$(dpkg-query -W -f '${db:Status-Status}' "$1" 2>/dev/null)" = installed ]; }

step "Installing stock Pro client and desktop tools"
apt-get update -q
apt-get install -y -q ubuntu-pro-client update-manager software-properties-gtk \
    xvfb xauth dbus > /dev/null
grep PRETTY_NAME /etc/os-release
removed=()
for p in $PRO_PKGS; do
    if installed "$p"; then
        removed+=("$p")
        echo "$p $(dpkg-query -W -f '${Version}' "$p")"
    fi
done

step "Installing $(dpkg-deb -f "$DEB" Package) $(dpkg-deb -f "$DEB" Version)"
apt-get install -y "$DEB"
installed fake-ubuntu-advantage-tools || fail "package not installed"
for p in $PRO_PKGS; do
    if installed "$p"; then fail "$p still installed"; fi
done
for p in update-manager software-properties-gtk; do
    installed "$p" || fail "$p was removed"
done
apt-get check

step "Python stubs"
(cd /tmp && python3 "$SRC/test_stubs.py")

step "D-Bus stub"
mkdir -p /run/dbus
dbus-daemon --system --fork
useradd -m tester
runuser -u tester -- dbus-send --system --print-reply \
    --dest=com.canonical.UbuntuAdvantage / \
    org.freedesktop.DBus.ObjectManager.GetManagedObjects

# App must still be running after the timeout, with no Python traceback
smoke() {
    local log=/tmp/smoke.log rc=0
    runuser -u tester -- env HOME=/home/tester \
        xvfb-run -a dbus-run-session -- timeout 20 "$@" > "$log" 2>&1 || rc=$?
    if grep -q Traceback "$log" || [ "$rc" -ne 124 ]; then
        cat "$log"
        fail "$1 exited with $rc"
    fi
    echo "$1 OK"
}

step "Launching apps"
smoke update-manager --no-update
smoke software-properties-gtk

# Reinstall everything the package replaced, or apt removes dependents
step "Restoring stock Pro client: ${removed[*]}"
apt-get install -y "${removed[@]}"
if installed fake-ubuntu-advantage-tools; then fail "package not replaced"; fi
for p in update-manager software-properties-gtk; do
    installed "$p" || fail "$p was removed"
done
apt-get check

step "All install tests passed"
