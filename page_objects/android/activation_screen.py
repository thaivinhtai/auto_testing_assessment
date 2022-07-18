#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedScreen


class ActivationScreen(BasedScreen):
    def __init__(self):
        super().__init__()
        self.activation_code_fields = \
            'xpath=//android.widget.EditText[contains(@content-desc,' \
            ' "activation_")]'
        self.next_button = \
            'xpath=//android.widget.TextView[@content-desc="next"]'

    def enter_activation_code(self, activation_code: str):
        self.driver.logger.info("Enter activation code.")
        self.driver.wait_explicit(condition="presence_of_all_elements_located",
                                  locator=self.activation_code_fields)
        for locator_, value_ in zip(
            self.driver.get_elements(self.activation_code_fields),
            activation_code
        ):
            locator_.send_keys(value_)

    def click_next_button(self):
        self.driver.logger.info("Click on Next button.")
        self._click_on_locator(locator=self.next_button)
