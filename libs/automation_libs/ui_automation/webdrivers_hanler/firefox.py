#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FireFox.
"""

from selenium import webdriver

import geckodriver_autoinstaller


def get_firefox(headless: bool = False, *args, **kwargs) -> webdriver:
    """This function establishes firefox browser."""
    firefox_options = webdriver.FirefoxOptions()
    if headless:
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--debug')
    firefox_options.set_preference("dom.push.enabled", False)
    geckodriver_autoinstaller.install()
    firefox_driver = webdriver.Firefox(options=firefox_options)
    if kwargs.get("extension"):
        firefox_driver.install_addon(kwargs.get("extension"), temporary=True)
    return firefox_driver
