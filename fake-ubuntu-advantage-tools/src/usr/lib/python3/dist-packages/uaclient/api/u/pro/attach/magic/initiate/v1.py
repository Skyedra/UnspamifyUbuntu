"""
Stub implementation of uaclient.api.u.pro.attach.magic.initiate.v1 module.

This is part of the fake-ubuntu-advantage-tools package that replaces
ubuntu-advantage-tools to remove advertisements from Ubuntu.

This stub provides minimal functionality to prevent crashes in Ubuntu
system tools (particularly software-properties-gtk) that import this module.
"""


class InitiateResult:
    """Stub class representing the result of a magic attach initiation."""
    
    def __init__(self, success=False, token="", user_code="", error=""):
        self.success = success
        self.token = token
        self.user_code = user_code
        self.error = error


def initiate():
    """
    Stub function that simulates initiating a magic attach operation.
    
    Since we've removed ubuntu-advantage-tools, there's no actual attach
    service to connect to. This returns empty strings to prevent crashes
    in GUI dialogs that expect string values.
    
    Returns:
        InitiateResult: An object with empty strings (operation not available)
    """
    return InitiateResult(
        success=False,
        token="",
        user_code="",
        error="Ubuntu Advantage not available"
    )


# For compatibility with different import styles
__all__ = ['initiate', 'InitiateResult']
