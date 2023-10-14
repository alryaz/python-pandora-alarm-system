"""Constants used throughout Pandora CAS Python API."""

__all__ = ("DEFAULT_USER_AGENT", "DEFAULT_CONTROL_TIMEOUT")

from typing import Final

DEFAULT_USER_AGENT: Final = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/60.0.3112.113 Safari/537.36"
)
"""default user agent for use in requests"""

DEFAULT_CONTROL_TIMEOUT: Final = 30
"""timeout to consider command execution unsuccessful"""
