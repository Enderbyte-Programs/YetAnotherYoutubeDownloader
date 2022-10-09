"""Shared functions between LXI programs."""
import os
import sys
def isinterminalenvironment() -> bool:
    """Checks if program can be run graphically"""
    if "DISPLAY" in os.environ:
        return False
    else:
        return True

def iscompiled() -> bool:
    """Checkes if program is compiled into an executable"""
    if getattr(sys, 'frozen', False):
        return False
    elif __file__:
        return True