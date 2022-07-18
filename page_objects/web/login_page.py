#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedPage


class LoginPage(BasedPage):
    def __init__(self):
        super().__init__()
        self.company_input_field = 'xpath=//input[@placeholder="Company"]'
        self.next_button = 'xpath=//*[contains(text(), "Next")]'
        self.username_input_field = \
            'xpath=//*[contains(@data-testid, "usernameLogin")]'
        self.password_input_field = \
            'xpath=//*[contains(@data-testid, "passwordLogin")]'
        self.login_button = 'xpath=//*[contains(@class, "Login_button")]'
        self.otp_input_fields = 'xpath=//input[contains(@type, "tel")]'

    def enter_company_name(self, company: str):
        self.driver.logger.info(f"Enter Company name as {company}")
        self._send_string_to_locator(locator=self.company_input_field,
                                     str_to_be_sent=company)

    def click_next_button(self):
        self.driver.logger.info("Click on Next button.")
        self._click_on_locator(locator=self.next_button)

    def login_with_username_password(self, username: str, password: str):
        self.driver.logger.info("Login with username and password.")
        for locator_, value_ in zip(
                (self.username_input_field, self.password_input_field),
                (username, password)
        ):
            self._send_string_to_locator(locator=locator_,
                                         str_to_be_sent=value_)
        self._click_on_locator(locator=self.login_button)

    def input_otp(self, otp_value: str):
        self.driver.logger.info("Input OTP.")
        for locator_, value_ in zip(
            self.driver.get_elements(self.otp_input_fields),
            otp_value
        ):
            locator_.send_keys(value_)

    def log_in(self, company: str, username: str, password: str, otp: str):
        self.driver.logger.info("Login user.")
        self.enter_company_name(company=company)
        self.click_next_button()
        self.login_with_username_password(username=username, password=password)
        self.input_otp(otp_value=otp)
