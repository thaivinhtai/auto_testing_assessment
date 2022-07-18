#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains function that generates log folders.
"""

from datetime import datetime
from os import mkdir, path

from config.common import LOG_DIR
from .runtime_variable_namespace import RuntimeVariable


TODAY = datetime.now().strftime("%Y-%m-%d")
CURRENT_TIME = datetime.now().strftime("%H-%M-%S")


def generate_current_time_execution_log_dir() -> None:
    """Create and return path of folder that stores current time log files.

    This function takes the timestamp when test cases are run, then create
    directories to store log files.

    The structure of generated folders:
        workspace/{today}/{current_time}

    Returns
    -------
    None
    """
    today_log_folder = f'{LOG_DIR}/{TODAY}'
    current_time_execution_log_dir = f'{today_log_folder}/{CURRENT_TIME}'

    for directory in (
            LOG_DIR, today_log_folder, current_time_execution_log_dir):
        if not path.exists(directory):
            try:
                mkdir(directory)
            except FileExistsError:
                continue

    allure_result_folder = f'{current_time_execution_log_dir}/allure-results'
    screenshot_folder = f'{current_time_execution_log_dir}/screenshots'

    mkdir(allure_result_folder)
    mkdir(screenshot_folder)

    RuntimeVariable.CURRENT_LOG_DIR = current_time_execution_log_dir
    RuntimeVariable.CURRENT_ALLURE_RESULT_DIR = allure_result_folder
