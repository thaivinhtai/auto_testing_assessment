#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module gets arguments via specified flags.
"""


import argparse

from config.common import DEFAULT_ANDROID_APP_PATH


def __get_args() -> argparse.Namespace:
    """Get test arguments.

    Returns
    -------
    argparse.Namespace
        browser : browser to execute test on
        device_name : device to test on
        android_ver : mobile platform version
        app : The path to an APK file
        debug : Use when debugging, when this flag is enable the
                test cases won't re-run on failure.
        stop_on_failure : Immediately stop the script when failure is happened
        retry_times : The amount of times to be re-run when test cases failed,
                      default = 2.
        run_allure : start allure reporting server after test.
    """
    parser = argparse.ArgumentParser(description='Test Execution arguments '
                                                 'handling')
    parser.add_argument('--browser', required=False,
                        default='chrome', help='Browser to be run')
    parser.add_argument('--device-name', required=False,
                        help='Android device to run test cases om')
    parser.add_argument('--android-ver', required=False,
                        help='Version of Android OS')
    parser.add_argument('--app', required=False,
                        default=DEFAULT_ANDROID_APP_PATH,
                        help='The path to an APK file.')
    parser.add_argument('--mobile-udid', required=False, default="",
                        help="The mobile device's udid.")
    parser.add_argument('--run-allure', required=False, action='store_true',
                        help='Run Allure report server in local')
    parser.add_argument('--appium-port', required=False, default='4723',
                        help='Specify port to run appium')
    parser.add_argument('--debug', required=False, action="store_true",
                        help="Use when debugging, when this flag is enable, "
                             "the test cases won't re-run on failure.")
    parser.add_argument('--stop-on-failure', required=False,
                        action="store_true", help=
                        "Immediately stop the script when failure is happened")
    parser.add_argument('--retry-times', required=False, default=2,
                        help="The amount of times to be re-run when test cases"
                             "failed, default=2")
    return parser.parse_args()


# This global variable stores value of __get_args(), this makes ArgumentParser
# be initialed just one time and store the argparse.Namespace that we can use
# later.

ARGUMENTS = __get_args()
