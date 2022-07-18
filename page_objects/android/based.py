#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Base module of the screen-objects.
"""

from abc import ABC

from libs.automation_libs.ui_automation.mobile_auto_lib import MOBILE_DRIVER


class BasedScreen(ABC):
    def __init__(self):
        self.driver = MOBILE_DRIVER
        self.default_timeout = 15

    def is_element_clickable(self, name: str, locator: str) -> bool:
        """Is element clickable.

        Check if an element is clickable and return True, if not, take a
        screenshot and return False

        Parameters
        ----------
        name : The name of element that is written in the debug log
        locator : The locator of element

        Returns
        -------
        bool
            True if element is clickable
            False if element is not found or not clickable
        """
        result = self.driver.wait_explicit(
            condition='element_to_be_clickable',
            locator=locator,
            timeout=self.default_timeout
        )
        self.driver.logger.debug(f'Check if the element with {name}'
                                 ' button is clickable.')
        if result:
            return result
        self.driver.logger.warn(f'The element {name} is not clickable.')
        self.driver.take_screenshot()
        return False

    def is_element_visible(self, name: str, locator: str) -> bool:
        """Is element visible.

        Check if an element is visible and return True, if not, take a
        screenshot and return False

        Parameters
        ----------
        name : The name of element that is written in the debug log
        locator : The locator of element

        Returns
        -------
        bool
            True if element is clickable
            False if element is not found or not clickable
        """
        result = self.driver.wait_explicit(
            condition='visibility_of_element_located',
            locator=locator,
            timeout=self.default_timeout
        )
        self.driver.logger.debug(f'Check if the element with {name}'
                                 ' button is visible.')
        if result:
            return result
        self.driver.logger.warn(f'The element {name} is not visible.')
        self.driver.take_screenshot()
        return False

    def _click_on_locator(self, locator: str, timeout: int = -1):
        self.driver.click_on_locator_with_wait_explicit(
            locator=locator, timeout=timeout)

    def _send_string_to_locator(self, locator: str, str_to_be_sent: str,
                                timeout: int = -1):
        self.driver.send_string_with_wait_explicit(
            locator=locator, str_to_be_sent=str_to_be_sent, timeout=timeout)
