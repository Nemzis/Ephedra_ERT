# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 23:13:54 2026

@author: Vladimir
"""

from pathlib import Path
import sys

ROOT = Path(sys.argv[0]).resolve().parent if getattr(sys, "frozen", False) \
       else Path(__file__).resolve().parent.parent


def get_path(*parts):
    return ROOT.joinpath(*parts)