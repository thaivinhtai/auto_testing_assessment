#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""


from getpass import getuser
from typing import Union

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry
from behave.model import ScenarioOutline, Scenario

from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choice, randint, uniform
from allure import attach
from allure_commons.types import AttachmentType
import allure

from libs.utils import LOGGER
from config.common import WORKSPACE_DIR


ALLURE_ATTACHMENT_TYPE = {
    'txt': AttachmentType.TEXT,
    'csv': AttachmentType.CSV,
    'tsv': AttachmentType.TSV,
    'uri': AttachmentType.URI_LIST,
    "html": AttachmentType.HTML,
    "xml": AttachmentType.XML,
    "json": AttachmentType.JSON,
    "yaml": AttachmentType.YAML,
    "yml": AttachmentType.YAML,
    "pcap": AttachmentType.PCAP,
    "png": AttachmentType.PNG,
    "jpg": AttachmentType.JPG,
    "svg": AttachmentType.SVG,
    "gif": AttachmentType.GIF,
    "bmp": AttachmentType.BMP,
    "tiff": AttachmentType.TIFF,
    "mp4": AttachmentType.MP4,
    "ogg": AttachmentType.OGG,
    "webm": AttachmentType.WEBM,
    "pdf": AttachmentType.PDF,
}
SCENARIO_DESCRIPTION = ""
SCENARIO_NAME = ""
SCENARIO_TAGS = ""


def expect_true(result: bool, failed_message: str = "", defect_code: str = "",
                ticket: str = "", instance: any = None) -> None:
    if ticket:
        allure.dynamic.link(url=ticket, link_type="link", name=ticket)
    if not result:
        if defect_code:
            allure.dynamic.issue(defect_code, defect_code)
        if instance:
            instance.driver.take_screenshot()
        raise AssertionError(failed_message if not defect_code
                             else f"Failed with defect: {defect_code}")


def log_current_executor() -> None:
    """Log current executor's info.

    This function helps to log current tester, who executes the test case.

    Returns
    -------
    None
    """
    current_user = getuser()
    current_dir = WORKSPACE_DIR
    LOGGER.info("", timestamp=False)
    LOGGER.info(f'Test case ' +
                f'is conducted by: {current_user}')
    LOGGER.info(f'Workspace locates at {current_dir}')
    LOGGER.info(f'========== Test Case Begins ==========')


def random_str(length: int) -> str:
    """Generate random string.

    This function generates random string with given length.

    Parameters
    ----------
    length : int
        Length of string to be generated.

    Returns
    -------
    string
        A random string.
    """
    letters = ascii_lowercase + ascii_uppercase + digits + punctuation
    return ''.join(choice(letters) for i in range(length))


def random_number(min_number=0, max_number=0) -> int:
    """Generate random number.

    This function generates a random min_number from 0 to max_number.

    Parameters
    ----------
    min_number : int
        The smallest number can be generated.
    max_number : int
        The largest number can be generated.

    Returns
    -------
    int
        A random number.
    """
    return randint(min_number, max_number)


def random_float_number(min_number: float = 0.0, max_number: float = 0.0,
                        ignore_0: bool = False) -> float:
    """Generate random number.

    This function generates a random number from min_number to max_number.

    Parameters
    ----------
    min_number : float
        The smallest number can be generated.
    max_number : float
        The largest number can be generated.
    ignore_0 : bool
        True will not return 0

    Returns
    -------
    float
        A random number.
    """
    result = uniform(min_number, max_number)
    if ignore_0:
        while result == 0.0:
            result = uniform(min_number, max_number)
    return uniform(min_number, max_number)


def attach_file_to_report(attachments: list) -> None:
    """Attach logfile in text to Allure report.

    Returns
    -------
    None
    """
    for attachment in attachments:
        try:
            attachment_file = open(attachment, 'rb')
            file_type = attachment.split("/")[-1].split('.')[-1]
            attach_file = attachment_file.read()
            attach(attach_file, name='attachment',
                   attachment_type=ALLURE_ATTACHMENT_TYPE.get(file_type))
            attachment_file.close()
        except FileNotFoundError as ex:
            print('Could not attach log file.', ex)


def retry_on_failure(scenario: any) -> None:
    """

    """
    patch_scenario_with_autoretry(scenario, max_attempts=1)


def set_default_test_case_behavior(scenario: any,
                                   tsm_link_mapping: dict = None) -> None:
    """

    """
    global SCENARIO_TAGS, SCENARIO_NAME
    SCENARIO_NAME = scenario.name
    SCENARIO_TAGS = str(scenario.tags) if scenario.tags else ""
    if tsm_link_mapping:
        scenario_id = SCENARIO_NAME.split("-")[0].strip().rstrip()
        allure.dynamic.link(url=tsm_link_mapping.get(scenario_id),
                            name=scenario_id)


def mapping_browser_name_and_device_with_scenario_outline(
        scenario_: Union[Scenario, ScenarioOutline], browser_name: str,
        device_name: str
) -> Union[Scenario, ScenarioOutline]:
    """

    Parameters
    ----------
    scenario_ : Union[Scenario, ScenarioOutline]
    browser_name : str
    device_name : str

    Returns
    -------

    """
    browser_name = browser_name.upper()
    device_name = device_name.upper()
    if type(scenario_) == Scenario:
        return scenario_
    for example_ in scenario_.examples:
        example_.table.rows[0].cells = [browser_name, device_name]
    for scenario in scenario_.scenarios:
        scenario.description = scenario_.description
    return scenario_
