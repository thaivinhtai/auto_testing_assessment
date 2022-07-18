#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedPage


class SideMenu(BasedPage):
    def __init__(self):
        super().__init__()
        self.profile_link_button = \
            'xpath=//*[contains(@data-testid, "link-to-profile")]'

    def open_to_user_profile(self):
        self.driver.logger.info("Open user profile.")
        self._click_on_locator(self.profile_link_button)
