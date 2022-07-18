#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""


from .based import BasedPage


class ProfileMenu(BasedPage):
    def __init__(self):
        super().__init__()
        self.devices_tab = 'xpath=//*[contains(text(), "Devices")]'

    def open_devices_page(self):
        self.driver.logger.info("Open Devices page.")
        self._click_on_locator(locator=self.devices_tab)
