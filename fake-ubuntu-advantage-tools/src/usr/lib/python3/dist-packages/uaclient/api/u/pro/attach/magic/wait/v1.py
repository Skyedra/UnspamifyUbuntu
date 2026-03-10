"""
Stub implementation of uaclient.api.u.pro.attach.magic.wait.v1 module.

This is part of the fake-ubuntu-advantage-tools package that replaces
ubuntu-advantage-tools to remove advertisements from Ubuntu.

This stub provides minimal functionality to prevent crashes in Ubuntu
system tools (particularly software-properties-gtk) that import this module.
"""


class MagicAttachWaitOptions:
    """Stub class representing options for magic attach wait operation."""
    
    def __init__(self, magic_token=None):
        self.magic_token = magic_token


class WaitResult:
    """Stub class representing the result of a magic attach wait operation."""
    
    def __init__(self, success=False, contract_token=None, error=None):
        self.success = success
        self.contract_token = contract_token
        self.error = error


def wait(options=None):
    """
    Stub function that simulates waiting for a magic attach operation to complete.
    
    Since we've removed ubuntu-advantage-tools, there's no actual attach
    service to wait for. This returns a failed result to prevent crashes.
    
    Args:
        options: MagicAttachWaitOptions (ignored in stub)
        
    Returns:
        WaitResult: An object indicating the operation is not available
    """
    return WaitResult(
        success=False,
        contract_token=None,
        error="Ubuntu Advantage not available"
    )


# For compatibility with different import styles
__all__ = ['wait', 'MagicAttachWaitOptions', 'WaitResult']
