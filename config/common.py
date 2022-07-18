#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Some common configs
"""

from pathlib import Path
from os import name


# Workspace dir
WORKSPACE_DIR = str(Path(__file__).parent.absolute().parent)

# Execution result folder path. Default {WORKSPACE_DIR}/logs
LOG_DIR = f'{WORKSPACE_DIR}/logs'

# Because of demo purposes, I do not parameterize the test cases or test suites
# The scenario files are set to default here.
BEHAVE_SCENARIO_DIR = f'{WORKSPACE_DIR}/test_scenarios/assessment'
BEHAVE_FEATURE_FILE = f'{BEHAVE_SCENARIO_DIR}/assessment.feature'

# Allure configs
ALLURE_CATEGORIES = f'{WORKSPACE_DIR}/config/allure/categories.json'
ALLURE_ENVIRONMENT = f'{WORKSPACE_DIR}/config/allure/environment.properties'
ALLURE_BIN = f'{WORKSPACE_DIR}/libs/tools/allure/bin/allure'
if name == 'nt':
    ALLURE_BIN += ".bat"

# Default Android app path
DEFAULT_ANDROID_APP_PATH = f'{WORKSPACE_DIR}/resource/app-qa-release.apk'
