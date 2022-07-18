#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from selenium.common.exceptions import NoSuchWindowException, \
    WebDriverException

from resource.common_variables import HOMEPAGE_URL
from .based import BasedPage


class HomePage(BasedPage):
    def __init__(self):
        super().__init__()

    def access_home_page_url(self):
        try:
            self.driver.go_to_url(HOMEPAGE_URL)
        except (NoSuchWindowException, WebDriverException):
            self.driver.close_session()
            self.access_home_page_url()
