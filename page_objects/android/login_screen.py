#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedScreen


class LoginScreen(BasedScreen):
    def __init__(self):
        super().__init__()
        self.password_field = \
            'xpath=//android.widget.EditText[@content-desc="login_password"]'
        self.sign_in_button = \
            'xpath=//android.widget.TextView[@content-desc="auth.sign_in"]'

    def enter_password(self, password: str):
        self.driver.logger.info("Enter password.")
        self._send_string_to_locator(locator=self.password_field,
                                     str_to_be_sent=password)

    def click_on_sign_in_button(self):
        self.driver.logger.info("Click on Sign In button.")
        self._click_on_locator(locator=self.sign_in_button)

    def log_in(self, password: str):
        self.driver.logger.info("Log in.")
        self.enter_password(password=password)
        self.click_on_sign_in_button()
