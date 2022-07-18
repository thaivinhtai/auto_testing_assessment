#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is for storing useful variable in runtime.
"""


class RuntimeVariable:
    CURRENT_LOG_DIR = ""
    CURRENT_ALLURE_RESULT_DIR = ""
    CURRENT_SCREENSHOT_DIR = ""


class AppiumProperties:

    def __init__(self, port: int = 4723):
        self.port = port
        self.mobile_udid = ""
        self.chrome_driver_port = self.port + 2000
        self.mjpeg_server_port = self.port + 3000
        self.system_port = self.port + 4000

    def get_appium_port(self):
        return self.port

    def get_mobile_udid(self):
        return self.mobile_udid

    def get_chrome_driver_port(self):
        return self.chrome_driver_port

    def get_mjpeg_server_port(self):
        return self.mjpeg_server_port

    def get_system_port(self):
        return self.system_port
