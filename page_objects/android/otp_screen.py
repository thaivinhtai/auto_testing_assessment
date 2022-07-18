#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedScreen


class OTPScreen(BasedScreen):
    def __init__(self):
        super().__init__()
        self.otp_fields = \
            'xpath=//android.widget.EditText[contains(@content-desc, "otp_")]'

    def enter_otp(self, otp_value: str):
        self.driver.logger.info("Enter activation code.")
        self.driver.wait_explicit(condition="presence_of_all_elements_located",
                                  locator=self.otp_fields)
        for locator_, value_ in zip(
            self.driver.get_elements(self.otp_fields),
            otp_value
        ):
            locator_.send_keys(value_)
