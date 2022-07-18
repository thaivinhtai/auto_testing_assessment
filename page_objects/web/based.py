#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from abc import ABC

from libs.automation_libs.ui_automation.web_auto_lib import WEB_DRIVER


class BasedPage(ABC):
    def __init__(self):
        self.driver = WEB_DRIVER

    def _click_on_locator(self, locator: str, timeout: int = -1):
        self.driver.click_on_locator_with_wait_explicit(
            locator=locator, timeout=timeout
        )

    def _send_string_to_locator(self, locator: str, str_to_be_sent: str):
        self.driver.send_string_with_wait_explicit(
            locator=locator,
            str_to_be_sent=str_to_be_sent)
