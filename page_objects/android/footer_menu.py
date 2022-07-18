#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedScreen


class FooterMenu(BasedScreen):
    def __init__(self):
        super().__init__()
        self.contact_tab = 'xpath=//*[@content-desc="bottomTab_contact"]'

    def click_on_contact_tab(self):
        self.driver.logger.info("Click on Contact Tab")
        self._click_on_locator(locator=self.contact_tab)
