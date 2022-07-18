#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedScreen


class WelcomeScreen(BasedScreen):
    def __init__(self):
        super().__init__()
        self.skip_button = 'xpath=//*[@content-desc="activation.skip"]'

    def open_app(self):
        self.driver.logger.info("Open app.")
        self.driver.set_driver()

    def click_on_skip_button(self):
        if not self.driver.driver:
            self.driver.set_driver()
        self.driver.logger.info("Click on Skip button")
        self._click_on_locator(self.skip_button)
