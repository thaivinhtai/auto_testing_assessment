#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedScreen
from libs.automation_libs.common_funcs import expect_true


class ContactScreen(BasedScreen):
    def __init__(self):
        super().__init__()
        self.search_bar = 'xpath=//*[@content-desc="contact_search"]'
        self.tab_team = \
            'xpath=//android.widget.TextView[@content-desc="chat.team"]'

    def search_for_user(self, username: str):
        self.driver.logger.info("Click on Contact Tab")
        self._send_string_to_locator(locator=self.search_bar,
                                     str_to_be_sent=username)

    def switch_to_tab_team(self):
        self.driver.logger.info("Switch to tab Team.")
        self._click_on_locator(locator=self.tab_team)

    def click_on_first_team_searching_result(self, keyword: str):
        self.driver.logger.info('Choose the first result after searching with '
                                f'keyword "{keyword}"')
        self.search_for_user(username=keyword)
        result_xpath = f'xpath=//*[contains(@content-desc, "{keyword}")]'
        self.driver.wait_explicit(condition="presence_of_all_elements_located",
                                  locator=result_xpath)
        result = self.driver.get_elements(result_xpath)
        if len(result) > 0:
            result[0].click()
            return True
        expect_true(False, instance=self,
                    failed_message="There is no such user.")
