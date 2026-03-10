"""
Stub implementation of uaclient.api.u.pro.packages.updates.v1 module.

This is part of the fake-ubuntu-advantage-tools package that replaces
ubuntu-advantage-tools to remove advertisements from Ubuntu.

This stub provides minimal functionality to prevent crashes in Ubuntu
system tools (like UpdateManager and software-properties-gtk) that
import this module.
"""


class UpdateInfo:
    """Stub class representing update information."""
    
    def __init__(self, package="", version="", download_size=0, status=""):
        self.package = package
        self.version = version
        self.download_size = download_size
        self.status = status


class UpdateResult:
    """Stub class representing the result of an updates query."""
    
    def __init__(self):
        # Return empty list - no Ubuntu Advantage updates available
        self.updates = []


def updates():
    """
    Stub function that returns an empty UpdateResult.
    
    This prevents Ubuntu system tools from crashing when they try to
    check for Ubuntu Advantage security updates. Since we've removed
    ubuntu-advantage-tools, there are no updates to report.
    
    Returns:
        UpdateResult: An object with an empty updates list
    """
    return UpdateResult()


# For compatibility with different import styles
__all__ = ['updates', 'UpdateInfo', 'UpdateResult']