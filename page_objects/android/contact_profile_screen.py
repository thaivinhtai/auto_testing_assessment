#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedScreen


class ContactProfileScreen(BasedScreen):
    def __init__(self):
        super().__init__()
        self.chats_button = \
            'xpath=//android.view.ViewGroup[@content-desc="profile_chat"]'

    def click_on_chat(self):
        self.driver.logger.info("Click on Chats")
        self._click_on_locator(locator=self.chats_button)
