#!/bin/bash
set -e

echo "=========================================="
echo "Building fake-ubuntu-advantage-tools"
echo "=========================================="
echo ""

# Check if src directory exists
if [ ! -d "./src" ]; then
    echo "Error: ./src directory not found!"
    exit 1
fi

# Check if DEBIAN/control exists
if [ ! -f "./src/DEBIAN/control" ]; then
    echo "Error: ./src/DEBIAN/control not found!"
    exit 1
fi

# Check if Python stubs exist
if [ ! -f "./src/usr/lib/python3/dist-packages/uaclient/api/u/pro/packages/updates/v1.py" ]; then
    echo "Error: Python stub files not found!"
    echo "Make sure the uaclient module structure is present in src/"
    exit 1
fi

echo "✓ Source directory structure verified"
echo ""

# Stage a copy with normalized permissions
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
cp -r ./src "$STAGE/pkg"
find "$STAGE/pkg" -name __pycache__ -type d -prune -exec rm -rf {} +
find "$STAGE/pkg" -type d -exec chmod 0755 {} +
find "$STAGE/pkg" -type f -exec chmod 0644 {} +
chmod 0755 "$STAGE/pkg/DEBIAN/postinst" "$STAGE/pkg/DEBIAN/postrm" \
    "$STAGE/pkg/usr/lib/ubuntu-advantage/ua-dbus-stub"

# Build the package (files must be owned by root, not the builder's uid)
echo "Building .deb package..."
dpkg-deb --root-owner-group -b "$STAGE/pkg" fake-ubuntu-advantage-tools.deb

echo ""
echo "=========================================="
echo "✓ Package built successfully!"
echo "=========================================="
echo ""
echo "Package: fake-ubuntu-advantage-tools.deb"
echo "Size: $(du -h fake-ubuntu-advantage-tools.deb | cut -f1)"
echo ""
echo "To verify the package contents, run:"
echo "  dpkg -I fake-ubuntu-advantage-tools.deb"
echo "  dpkg -c fake-ubuntu-advantage-tools.deb"
echo ""
echo "To install the package, run:"
echo "  sudo apt install ./fake-ubuntu-advantage-tools.deb"
echo ""
