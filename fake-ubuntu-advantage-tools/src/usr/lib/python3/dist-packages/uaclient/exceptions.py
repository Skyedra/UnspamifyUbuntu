"""
Stub implementation of uaclient.exceptions module.

This is part of the fake-ubuntu-advantage-tools package that replaces
ubuntu-advantage-tools to remove advertisements from Ubuntu.

This stub provides minimal exception classes to prevent crashes in Ubuntu
system tools (particularly software-properties-gtk) that import this module.
"""


class UbuntuProError(Exception):
    """Base exception class for Ubuntu Pro errors."""
    pass


class MagicAttachTokenError(UbuntuProError):
    """
    Exception raised when magic attach token operations fail.
    
    This is used by software-properties-gtk when polling for magic attach
    tokens times out or encounters errors.
    """
    pass


class AttachError(UbuntuProError):
    """Exception raised when attach operations fail."""
    pass


class DetachError(UbuntuProError):
    """Exception raised when detach operations fail."""
    pass


class ConfigError(UbuntuProError):
    """Exception raised for configuration errors."""
    pass


class EntitlementError(UbuntuProError):
    """Exception raised for entitlement-related errors."""
    pass


# For compatibility with different import styles
__all__ = [
    'UbuntuProError',
    'MagicAttachTokenError',
    'AttachError',
    'DetachError',
    'ConfigError',
    'EntitlementError',
]