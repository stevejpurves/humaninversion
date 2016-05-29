"""Utility functions."""

import sys
import os


def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))
