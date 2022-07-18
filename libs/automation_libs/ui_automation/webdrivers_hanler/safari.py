#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Safari.
"""

from selenium import webdriver


def get_safari(*args, **kwargs) -> webdriver:
    """This function establishes Safari browser."""
    return webdriver.Safari()
