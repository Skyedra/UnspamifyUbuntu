"""
Stub implementation of uaclient.api.u.pro.status module.

This is part of the fake-ubuntu-advantage-tools package that replaces
ubuntu-advantage-tools to remove advertisements from Ubuntu.

This stub provides minimal functionality to prevent crashes in Ubuntu
system tools that import this module.
"""


class StatusResult:
    """Stub class representing the status of Ubuntu Pro."""
    
    def __init__(self):
        self.attached = False
        self.enabled_services = []
        self.available_services = []
        self.account = None
        self.subscription = None


def status():
    """
    Stub function that returns Ubuntu Pro status.
    
    Since we've removed ubuntu-advantage-tools, there's no active subscription.
    This returns a status indicating the system is not attached.
    
    Returns:
        StatusResult: An object indicating no Ubuntu Pro subscription
    """
    return StatusResult()


# For compatibility with different import styles
__all__ = ['status', 'StatusResult']