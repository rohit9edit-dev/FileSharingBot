# plugins/__init__.py

"""
Plugins package

Yahan se saare individual feature plugins ko import/export kiya ja sakta hai.
"""

from .vault import VaultPlugin
from .self_destruct import SelfDestructPlugin
from .watermark import WatermarkPlugin
from .experimental import ExperimentalPlugin

__all__ = [
    "VaultPlugin",
    "SelfDestructPlugin",
    "WatermarkPlugin",
    "ExperimentalPlugin",
]
