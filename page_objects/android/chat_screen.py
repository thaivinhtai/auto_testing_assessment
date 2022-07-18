#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from .based import BasedScreen
from libs.automation_libs.ui_automation.mobile_auto_lib import KEYCODE_MAPPING
from appium.webdriver.common.touch_action import TouchAction


class ChatScreen(BasedScreen):
    def __init__(self):
        super().__init__()
        self.chat_box = \
            'xpath=//android.widget.TextView[@content-desc="send_to_room"]'
        self.send_message_button = \
            'xpath=//android.view.ViewGroup' \
            '[@content-desc="chatDetail_sendMessage"]'
        self.reply_button = \
            'xpath=//android.view.ViewGroup[@content-desc="reply"]'

    def click_on_chat_box(self):
        self.driver.logger.info("Click on Chat box")
        self._click_on_locator(locator=self.chat_box)

    def type_message(self, message: str):
        self.driver.logger.info("Type message")
        index = 0
        for char_ in message:
            if char_.isupper() and index != 0:
                self.driver.driver.press_keycode(
                    KEYCODE_MAPPING.get("shift_left")
                )
            self.driver.driver.press_keycode(
                KEYCODE_MAPPING.get(char_.lower()))
            index += 1

    def click_on_send_message_button(self):
        self.driver.logger.info("Click on Send message button")
        self._click_on_locator(locator=self.send_message_button)

    def send_message(self, message: str):
        self.driver.logger.info("Send message.")
        self.click_on_chat_box()
        self.type_message(message=message)
        self.click_on_send_message_button()
        device_time = self.driver.driver.get_device_time("HH:mm")
        print(device_time)
        return message, device_time

    def reply_message(self, message_to_reply: str, reply_message):
        actions = TouchAction(self.driver.driver)
        message_locator = \
            f'//android.widget.TextView[@content-desc="{message_to_reply}"]'
        self.driver.wait_explicit(condition="presence_of_element_located",
                                  locator=f'xpath={message_locator}')
        message_element = self.driver.get_element(f'xpath={message_locator}')
        actions.long_press(message_element)
        actions.perform()
        self._click_on_locator(locator=self.reply_button)
        self.send_message(message=reply_message)
