#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedPage

from libs.automation_libs.common_funcs import expect_true


class DevicesPage(BasedPage):
    def __init__(self):
        super().__init__()
        self.link_device_button = 'xpath=//*[contains(text(), "Link Device")]'
        self.activation_code = 'xpath=//*[contains(@class, "code-name")]'

    def click_on_link_device(self):
        self.driver.logger.info("Click on link Device.")
        self._click_on_locator(locator=self.link_device_button)

    def get_activation_code(self):
        self.driver.logger.info("Get Activation code.")
        result = self.driver.wait_explicit(
            condition="visibility_of_element_located",
            locator=self.activation_code, timeout=20
        )
        expect_true(result=result, instance=self,
                    failed_message="Can not get Activation code.")
        return self.driver.get_element(self.activation_code).text
