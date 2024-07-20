"""
@author: mira-6
@title: mira-wildcard-node
@nickname: mira-wildcard-node
@description: Single-node wildcard implementation.
"""
from . import custom_wildcard
NODE_CLASS_MAPPINGS = {
    **custom_wildcard.NODE_CLASS_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **custom_wildcard.NODE_DISPLAY_NAME_MAPPINGS,
}