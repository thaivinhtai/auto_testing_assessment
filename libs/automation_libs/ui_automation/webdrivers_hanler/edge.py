#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Edge.
"""

from os import listdir

from subprocess import Popen, PIPE

from selenium import webdriver

from edgedriver_autoinstaller import get_edge_version
from edgedriver_autoinstaller.utils import (
    get_platform_architecture as get_platform_architecture_edge, check_version,
    get_matched_edgedriver_version, get_edgedriver_url, get_edgedriver_filename
)

from ._chromium import __CURRENT_DIR, download_chromium_driver, \
    get_chromium_driver


def get_edgedriver():
    """Get edgedriver.

    Check if there is a edgedriver corresponding to the current edge
    version. If not, auto download the corresponding one.

    Returns
    -------
    str
        Absolute path to the edgedriver.
    """
    # Check platform and architect of machine's OS
    platform, architect = get_platform_architecture_edge()

    # Get edge version on local machine
    if platform != "mac":
        current_client_edge_version = get_edge_version()
    else:
        process = Popen(
            ['/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
             '--version'], stdout=PIPE)
        current_client_edge_version = process.communicate()[0]\
            .decode('UTF-8').replace('Microsoft Edge', '').strip()
    # Get edgedriver that is needed for automation
    edgedriver_version = \
        get_matched_edgedriver_version(current_client_edge_version)

    # edgedriver_folder = inter_path().edge_driver_dir
    edgedriver_folder = \
        f'{__CURRENT_DIR}/../../../tools/web_drivers'
    # Check if there is an existed edgedriver could be used
    for file_ in listdir(edgedriver_folder):
        if check_version(
                f'{edgedriver_folder}/{file_}',
                edgedriver_version) or check_version(
                    f'{edgedriver_folder}/{file_}',
                    current_client_edge_version):
            return f'{edgedriver_folder}/{file_}'

    # Get edgedriver download url
    edgedriver_download_url = get_edgedriver_url(edgedriver_version)
    edgedriver_download_url_backup = get_edgedriver_url(
        current_client_edge_version)

    return download_chromium_driver(
        platform=platform, architect=architect, chromium_distro="edge",
        chromium_version=edgedriver_version,
        current_client_chromium_version=current_client_edge_version,
        chromium_download_url=edgedriver_download_url,
        chromium_download_url_backup=edgedriver_download_url_backup,
        chromium_driver_folder=edgedriver_folder,
        get_chromium_driver_file_name=get_edgedriver_filename
    )


def get_edge(headless: bool = False, *args, **kwargs) -> webdriver:
    """This function establishes edge browser."""
    edge_options = webdriver.EdgeOptions()
    edge_options.use_chromium = True
    return get_chromium_driver(
        chromium_options=edge_options, chromium_driver=webdriver.Edge,
        headless=headless, extension=kwargs.get("extension"),
        driver=get_edgedriver()
    )
