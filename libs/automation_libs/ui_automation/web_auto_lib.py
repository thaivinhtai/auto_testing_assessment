#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains functions and abstract class for the keywords lib in every
testing module.
"""

from time import sleep

from selenium.webdriver.common.by import By

from libs.utils import LOGGER, ARGUMENTS
from .ui_based_class import AbstractDriver

from .webdrivers_hanler import get_chrome, get_edge, get_safari, get_firefox, \
    get_brave


def get_browser(name: str, headless: bool,
                browserstack: bool = False, **kwargs):
    """This function is used for quick selection of browser."""
    name = name.lower()
    switcher = {
        "firefox": get_firefox,
        "chrome": get_chrome,
        "edge": get_edge,
        "safari": get_safari,
        "brave": get_brave,
    }
    func = switcher.get(name)
    if browserstack:
        func = switcher.get("browserstack")
    return func(headless, **kwargs)


class WebFundamentalAction(AbstractDriver):
    """
    This abstract class is a blueprint for common keyword for each testing
    module.
    """

    def __init__(self):
        """Constructor."""
        super().__init__(By)
        self.logger = LOGGER
        self.undetected = False
        self.extension = ""
        self.browser = ARGUMENTS.browser
        self.headless = False if ARGUMENTS.debug else True

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.close_browser()

    def initial_webdriver_session(self):
        self.driver = get_browser(self.browser, self.headless,
                                  extension=self.extension,
                                  undetected=self.undetected)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.logger.info('', timestamp=False)
        self.logger.info(f'Open {self.browser.upper()} browser')

    def close_browser(self):
        self.driver.close()
        self.logger.info('Close browser tab.')

    def close_session(self):
        self.logger.info('Close session.')
        self.extension = ""
        self.driver.quit()
        self.driver = None

    def add_extension(self, extension: str):
        self.extension = extension

    def go_to_url(self, url: str):
        if not self.driver:
            self.initial_webdriver_session()
        self.driver.get(url)
        self.logger.info('', timestamp=False)
        self.logger.info(f'Access {url}')

    def read_alert_box_message(self) -> str:
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text

    def is_page_fully_loaded(self) -> bool:
        state = self.driver.execute_script("return document.readyState")
        page_source_1 = self.driver.page_source
        sleep(1)
        page_source_2 = self.driver.page_source
        complete_page_source = page_source_1 == page_source_2
        return state and complete_page_source


WEB_DRIVER = WebFundamentalAction()
