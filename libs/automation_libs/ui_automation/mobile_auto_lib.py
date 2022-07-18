#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contain custom keyword for mobile testing."""

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction

from selenium.webdriver.common.utils import is_url_connectable

from .ui_based_class import AbstractDriver
from libs.utils import ARGUMENTS
from config.common import WORKSPACE_DIR


class MobileFundamentalAction(AbstractDriver):
    """

    """

    def __init__(self):
        """

        Parameters
        ----------
        # platform_name
        # platform_version
        # device_name
        # app_package
        # app_activity
        """
        super().__init__(MobileBy)
        self.device_name = ARGUMENTS.device_name
        self.default_timeout = '40000'
        self.platform = "android"

        self.platform_version = ARGUMENTS.android_ver

        self.port_to_listen = ARGUMENTS.appium_properties.port

        self.element_mapping.update({
            'accessibility_id': self.context_by.ACCESSIBILITY_ID,
            'image': self.context_by.IMAGE
        })
        self.appium_remote_server = \
            f'http://127.0.0.1:{self.port_to_listen}/wd/hub'

        self.init_package = None
        self.init_activity = None

        self.window_size = None
        self.width = None
        self.height = None
        self.appium_server_session = None
        self.context = None
        self.contexts = None
        self.desired_cap = {}

    def set_driver(self):
        self.desired_cap.update({
            'platformName': self.platform,
            'platformVersion': self.platform_version,
            'deviceName': self.device_name,
            'udid': ARGUMENTS.appium_properties.mobile_udid,
            'fullReset': True if not ARGUMENTS.debug else False,
            'enablePerformanceLogging': True if not ARGUMENTS.debug else False,
            'ignoreUnimportantViews': True,
            'app': ARGUMENTS.app,
            'automationName': 'UIAutomator2',
            'adbExecTimeout': self.default_timeout,
            'newCommandTimeout': self.default_timeout,
            'autoGrantPermissions': True,
            'chromedriverExecutableDir':
                f"{WORKSPACE_DIR}/libs/tools/web_drivers",
            'chromedriverChromeMappingFile':
                f"{WORKSPACE_DIR}/libs/tools/web_drivers"
                f"/chrome_mapping_version.json",
            'chromedriverPort': ARGUMENTS.appium_properties.chrome_driver_port,
            'mjpegServerPort': ARGUMENTS.appium_properties.mjpeg_server_port,
            'systemPort': ARGUMENTS.appium_properties.system_port
        })

        self.driver = webdriver.Remote(self.appium_remote_server,
                                       self.desired_cap)
        self.init_activity = self.driver.current_activity
        self.init_package = self.driver.current_package
        self.window_size = self.driver.get_window_size()
        self.width = self.window_size.get("width")
        self.height = self.window_size.get("height")
        self.context = self.driver.context
        self.contexts = self.driver.contexts
        self.logger.info('', timestamp=False)
        self.logger.info(
            f'Execute test on {self.device_name}, platform {self.platform} '
            f'version {self.platform_version}'
        )

    def switch_context(self, context_name: str) -> None:
        """Switch context.

        Parameters
        ----------
        context_name : str

        Returns
        -------
        None
        """
        self.logger.debug(f'Current context: {self.driver.context}')
        self.logger.debug(f'Available contexts: {self.driver.contexts}')
        self.driver.switch_to.context(context_name)
        self.logger.debug(f'Switched to {context_name} context')

    def click_on_coordinate(self, coordinate) -> bool:
        """

        Parameters
        ----------
        coordinate

        Returns
        -------

        """
        action = TouchAction(self.driver)
        x = float(coordinate.get("x")) * self.width
        y = float(coordinate.get("y")) * self.height
        action.tap(x=x, y=y)
        self.logger.debug(f"Click on coordinate: (x={x}, y={y})")
        return True

    def swipe_horizontal(self, start: float = 0.9, end: float = 0.1) -> bool:
        """

        Parameters
        ----------
        start
        end

        Returns
        -------

        """
        self.driver.swipe(start_y=self.height*0.5, end_y=self.height*0.5,
                          start_x=self.width*start, end_x=self.width*end)
        return True

    def swipe_vertical(self, start: float = 0.9, end: float = 0.1) -> bool:
        """

        Parameters
        ----------
        start
        end

        Returns
        -------

        """
        self.driver.swipe(start_y=self.height*start, end_y=self.height*end,
                          start_x=self.width*0.5, end_x=self.width*0.5)
        return True

    def go_to_url(self, url: str):
        if not self.driver:
            self.set_driver()
        self.driver.get(url)
        self.logger.info('', timestamp=False)
        self.logger.info(f'Access {url}')

    def end_session(self):
        self.logger.info('End session.')
        self.driver.quit()
        self.driver = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close_app()
        self.logger.debug('Close app')
        self.driver.quit()
        self.logger.debug('End session')


KEYCODE_MAPPING = {
    'a': 29,
    'd': 32,
    'e': 33,
    'g': 35,
    'l': 40,
    'm': 41,
    'n': 42,
    'o': 43,
    'r': 46,
    's': 47,
    't': 48,
    '2': 2,
    'shift_left': 59,
    ' ': 62
}


MOBILE_DRIVER = MobileFundamentalAction()


if __name__ == "__main__":
    print(type(is_url_connectable(4723)))
