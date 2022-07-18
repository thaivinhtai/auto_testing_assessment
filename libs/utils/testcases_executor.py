#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module handles test cases execution.
"""

from subprocess import run
from os import name
from shutil import copyfile

from .process_executor import run_android_emulator, \
    execute_behave_test_cases, run_appium_server,\
    run_allure_report_server, create_latest_combined_log
from .log_dirs_generator import generate_current_time_execution_log_dir
from .runtime_variable_namespace import AppiumProperties, RuntimeVariable
from .args_parser import ARGUMENTS
from config.common import LOG_DIR


def execute_test_cases() -> None:
    """Execute test cases.

    This function gets arguments and calls module process_executor to run test
    cases.

    Returns
    -------
    None
    """
    debug = ARGUMENTS.debug

    appium_properties = AppiumProperties(int(ARGUMENTS.appium_port))
    ARGUMENTS.appium_properties = appium_properties
    platform_ver = ARGUMENTS.android_ver
    mobile_device = ARGUMENTS.device_name

    generate_current_time_execution_log_dir()

    emulator_session = run_android_emulator(
        device_name=mobile_device, debug=debug, version=platform_ver
    )
    appium_session, appium_log = run_appium_server(appium_properties)

    execute_behave_test_cases(debug=debug,
                              stop_on_failure=ARGUMENTS.stop_on_failure)

    # Export latest combined logs
    create_latest_combined_log()

    if appium_session:
        appium_log.flush()
        appium_session.terminate()
        appium_session.wait()
        appium_log.close()
        copyfile(
            f'{RuntimeVariable.CURRENT_LOG_DIR}'
            f'/appium-{appium_properties.port}.log',
            f'{LOG_DIR}/latest_combined_log'
            f'/appium-{appium_properties.port}.log'
        )

    if emulator_session:
        try:
            emulator_session.terminate()
            emulator_session.wait()
            emulator_session.kill()
        except PermissionError:
            if name != 'nt':
                pid = emulator_session.pid
                print('Force kill process with admin role.')
                run(['sudo', 'kill', '-9', f'{pid}'])
            else:
                print('Can not terminate emulator.')

    if ARGUMENTS.run_allure:
        allure_local_session = run_allure_report_server()
        input("Press any key to end the Allure report session.")
        allure_local_session.terminate()
        allure_local_session.wait()
