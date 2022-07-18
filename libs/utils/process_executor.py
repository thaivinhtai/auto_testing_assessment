#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module handles call to other processes.

    Functions in this module:

        +   create_empty_file(path_to_file: str) -> None
                Create empty file.

        +   copy_files(source_path: str, des_path: str) -> None
                Copy all items of a folder to other folder.

        +   generate_allure_report() -> None
                Generate allure report

        +   run_allure_report_server() -> None
                Open Allure report.

        +   run_appium_server() -> Popen
                Run Appium server.

        +   run_android_emulator(name: str) -> Popen
                Run Android emulator

"""

from os import kill, environ, system, listdir, path, name, mkdir, chdir

if name == "posix":
    from os import O_NONBLOCK
    import fcntl

from signal import SIGTERM
from subprocess import Popen, PIPE, run
from time import sleep
from sys import stdout
from shutil import copyfile, rmtree, copy2, copytree

from io import StringIO

from requests import request
from requests.exceptions import ConnectionError, ConnectTimeout

import sys
import contextlib

from typing import Union

from behave.__main__ import main as behave_main
from behave.step_registry import registry

from config.common import BEHAVE_SCENARIO_DIR, BEHAVE_FEATURE_FILE, \
    ALLURE_CATEGORIES, ALLURE_ENVIRONMENT, LOG_DIR, ALLURE_BIN
from .runtime_variable_namespace import RuntimeVariable
from .args_parser import ARGUMENTS


def check_appium_session(port: int) -> dict:
    """Check appium session.

    This function checks if appium server is running and there is session here.

    Returns
    -------
    dict
        appium_server : bool
        available_session : bool
    """
    available_session = False
    appium_server = False
    try:
        response = request(
            method='GET', timeout=1,
            url=f'http://127.0.0.1:{port}/wd/hub/sessions')
        if response.status_code == 200:
            appium_server = True
        if response.json().get('value'):
            available_session = True
        return {'appium_server': appium_server,
                'available_session': response.json().get('value')}
    except (ConnectTimeout, ConnectionError):
        pass
    return {'appium_server': appium_server,
            'available_session': available_session}


def print_progress_bar(wait_time: float, progress_status: str,
                       done: bool = False) -> None:
    """Print progress bar.

    This function visible the progress on console.

    Parameters
    ----------
    wait_time : float
        total time to wait.
    progress_status : str
        Status of the process.
    done : bool
        If done, progress bar shows 100%
    """

    def progress_bar(count: int, total: float, status: str):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        stdout.flush()

    increase = 0.01
    total_progress = wait_time / increase
    counter = 0
    while counter < total_progress:
        if done:
            counter = total_progress
        progress_bar(counter, total_progress, progress_status)
        sleep(increase)  # emulating long-playing job
        counter += 1


def create_empty_file(path_to_file: str) -> None:
    """Create an empty file.

    This function creates an empty file with specified path.

    Parameters
    ----------
    path_to_file : str
        Should be a full path to file.

    Returns
    -------
    None
    """
    with open(path_to_file, 'w'):
        pass


def copy_files(source_path: str, des_path: str, symlinks: bool = False,
               ignore=None) -> None:
    """Copy all file in source directory to an other directory.

    Parameters
    ----------
    source_path : str
        Path of source directory.
    des_path : str
        Path of des-directory.
    symlinks : bool
    ignore

    Returns
    -------
    None
    """
    for item in listdir(source_path):
        source = path.join(source_path, item)
        dest = path.join(des_path, item)
        if path.isdir(source):
            copytree(source, dest, symlinks, ignore)
        else:
            copy2(source, dest)


def execute_behave_test_cases(
        debug: bool = False, stop_on_failure: bool = False) -> None:
    """Execute behave test cases.

    This function call the python behave and export log.

    Parameters
    ----------
    debug : bool
        True to debug.
    stop_on_failure : Immediately stop the test script.

    Returns
    -------
    None
    """

    class TeeIO:
        def __init__(self, original, target):
            self.original = original
            self.target = target

        def write(self, b):
            open(f"{RuntimeVariable.CURRENT_LOG_DIR}/execution.log", "a+")\
                .write(b)
            self.original.write(b)
            self.target.write(b)

        def flush(self):
            self.original.flush()

    @contextlib.contextmanager
    def tee_stdout(target):
        tee = TeeIO(sys.stdout, target)
        with contextlib.redirect_stdout(tee):
            yield

    feature_dir = BEHAVE_SCENARIO_DIR
    feature_file = BEHAVE_FEATURE_FILE

    log_level = "INFO"
    if debug:
        log_level = "DEBUG"

    pretty_run_log = "--format=pretty --summary"

    stop = ""
    if stop_on_failure:
        stop = "--stop"

    while '\\' in feature_file:
        feature_file = feature_file.replace('\\', '/')

    output_result_dir = RuntimeVariable.CURRENT_ALLURE_RESULT_DIR
    while '\\' in output_result_dir:
        output_result_dir = output_result_dir.replace("\\", '/')

    junit_report_dir = RuntimeVariable.CURRENT_LOG_DIR
    while '\\' in junit_report_dir:
        junit_report_dir = junit_report_dir.replace("\\", '/')

    chdir(feature_dir)
    buf = StringIO()
    with tee_stdout(buf):
        execute_command = (
            f"--logging-level {log_level} --show-timings "
            f"--format allure_behave.formatter:AllureFormatter "
            f"--junit {pretty_run_log} --summary --no-logcapture -D "
            "AllureFormatter.issue_pattern="
            "https://foo.bar/browse/{} -D "
            "AllureFormatter.link_pattern="
            "https://foo.bar/{} "
            f'-o "{output_result_dir}" --junit-directory '
            f'"{junit_report_dir}" {stop} {feature_file}'
        )
        behave_main(execute_command)
    del buf
    registry.steps = {"given": [], "when": [], "then": [], "step": []}

    copyfile(ALLURE_CATEGORIES,
             f"{RuntimeVariable.CURRENT_ALLURE_RESULT_DIR}/categories.json")
    copyfile(
        ALLURE_ENVIRONMENT,
        f"{RuntimeVariable.CURRENT_ALLURE_RESULT_DIR}/environment.properties")


def create_latest_combined_log() -> None:
    """Create latest combined log.

    Combine all output.xml from all current execution suite in to one xml.

    Returns
    -------
    None
    """
    latest_combined_log_path = f"{LOG_DIR}/latest_combined_log"

    if not path.exists(latest_combined_log_path):
        mkdir(f"{LOG_DIR}/latest_combined_log")

    collect_current_allure_result_and_generate_report()


def _get_all_result_files_in_current_execution() -> tuple:
    """Get all result files in current execution.

    This function gets all files name and their absolute path of Allure result
    in current execution time.

    Returns
    -------
    tuple
        (result_files - list of absolute path to files,
         files - list name of files)
    """
    result_dir = RuntimeVariable.CURRENT_ALLURE_RESULT_DIR

    result_files = list()
    files = list()
    meta_data = ['categories.json', 'environment.properties']
    files += [file for file in listdir(result_dir)
              if file not in meta_data]
    result_files += [f'{result_dir}/{file}' for file in listdir(result_dir)
                     if file not in meta_data]

    files += meta_data
    result_files += [ALLURE_CATEGORIES, ALLURE_ENVIRONMENT]
    return result_files, files


def collect_current_allure_result_and_generate_report() -> None:
    """Collect current Allure result and generate report.

    Collect all the Allure result, copy it to temp folder and then generate
    Allure report.

    Returns
    -------
    None
    """
    if not path.exists(f"{LOG_DIR}/latest_combined_log/allure"):
        mkdir(f"{LOG_DIR}/latest_combined_log/allure")

    temp_allure_result = f"{LOG_DIR}/latest_combined_log/allure/result"
    temp_allure_report = f"{LOG_DIR}/latest_combined_log/allure/report"

    if path.exists(temp_allure_result):
        rmtree(temp_allure_result)

    result_files, files = \
        _get_all_result_files_in_current_execution()
    mkdir(temp_allure_result)

    for full_path, file_name in zip(result_files, files):
        copyfile(full_path, f"{temp_allure_result}/{file_name}")

    try:
        allure_local_generating = Popen(
            ['allure', 'generate', temp_allure_result,
             '--output', temp_allure_report, '--clean'],
            env=environ
        )
    except FileNotFoundError:
        allure_local_generating = Popen(
            [ALLURE_BIN, 'generate', temp_allure_result,
             '--output', temp_allure_report, '--clean'],
            env=environ
        )
    print_progress_bar(
        wait_time=3,
        progress_status=f"Generating Allure local report."
    )
    allure_local_generating.wait()


def run_allure_report_server() -> Popen:
    """Run Allure report server.

    This function run Allure server with the latest log information.

    Returns
    -------
    Popen
        allure session
    """
    temp_allure_report = f"{LOG_DIR}/latest_combined_log/allure/report"

    allure_local_session = \
        Popen([ALLURE_BIN, 'open', temp_allure_report], env=environ)
    print_progress_bar(
        wait_time=2,
        progress_status=f"Starting Allure local report."
    )
    return allure_local_session


def run_appium_server(port: any) -> tuple:
    """Run Appium server.

    Call Appium sever.

    Parameters
    ----------
    port : AppiumProperties
        Port to be started appium on.

    Returns
    -------
    tuple
        Appium session, logfile
    """
    result = check_appium_session(port.port)
    if not result.get('appium_server'):
        try:
            free_port(port.port)
        except (ProcessLookupError, PermissionError) as error:
            raise Exception(f"Could not kill process using port {port.port}."
                            f"{error}")
    if result.get('appium_server') and not result.get('available_session'):
        return None, None
    if result.get('available_session'):
        port.chrome_driver_port += len(result.get('available_session'))
        port.mjpeg_server_port += len(result.get('available_session'))
        port.system_port += len(result.get('available_session'))
        return None, None
    appium_log_file = \
        f'{RuntimeVariable.CURRENT_LOG_DIR}/appium-{port.port}.log'
    appium_log = open(appium_log_file, 'a')
    appium_log.flush()
    appium_command = ['appium']
    if name == "nt":
        appium_command = ['appium.cmd']
    appium_session = Popen([*appium_command, "--port", str(port.port),
                            '--allow-insecure', 'chromedriver_autodownload'],
                           stdout=appium_log, stderr=appium_log, env=environ)

    print_progress_bar(
        wait_time=3,
        progress_status=f"Starting Appium server on port {port.port}."
    )
    while True:
        if 'Appium REST http interface listener started' in \
                open(appium_log_file).read():
            break
        sleep(1)
    return appium_session, appium_log


def get_attached_android_devices() -> list:
    """Get attached Android devices.

    Returns
    -------
    list
        list of attached devices name.
    """
    command = ['adb', 'devices']
    splitter = '\r'
    is_shell = True
    if name == 'nt':  # For Window 10 user
        command = ["cmd", "/c"] + command
        splitter = '\r\n'
    if name == 'posix':  # For MacOS user
        splitter = '\n'
        is_shell = False
    run(command)
    c = Popen(command, shell=is_shell, stdout=PIPE, stderr=PIPE)
    standard_out, _ = c.communicate()
    output = standard_out.decode().strip().split(splitter)
    output.pop(0)
    for index, line in enumerate(output):
        output[index] = line.replace(line[line.find('\t'):], "")
    return output


def get_available_emulators() -> list:
    """Get available emulator.

    Returns
    -------
    list
        list of available emulators.
    """
    command = ['emulator', '-list-avds']
    splitter = '\r'
    is_shell = True
    if name == 'nt':  # For window
        command = ["cmd", "/c"] + command
        splitter = '\r\n'
    if name == 'posix':  # For MacOS 12
        is_shell = False
        splitter = '\n'
    c = Popen(command, shell=is_shell, stdout=PIPE, stderr=PIPE)
    standard_out, _ = c.communicate()
    output = standard_out.decode().strip().split(splitter)
    return output


def get_emulators_real_name(list_devices: list) -> list:
    """Get emulators real name.

    Parameters
    ----------
    list_devices : list
        List of attached devices that is got from adb devices command.

    Returns
    -------
    list
        List of emulators with their real names.
    """

    command = ['adb', '-s', None, 'emu', 'avd', 'name']
    index = 2
    is_shell = True
    splitter = '\r\r\n'
    if name == 'nt':  # For Window user
        command = ["cmd", "/c"] + command
        index += 2
    if name == 'posix':  # For MacOS user
        is_shell = False
        splitter = '\r\n'
    emulator_names = []
    for device_name in list_devices:
        command[index] = device_name
        c = Popen(command, shell=is_shell, stdout=PIPE, stderr=PIPE)
        standard_out, _ = c.communicate()
        output = standard_out.decode().strip().split(splitter)[0]
        emulator_names.append(output)
    return emulator_names


def run_android_emulator(**kwargs) -> Union[Popen, None]:
    """Run Android emulator.

    Run an Android emulator base on provided name.

    Parameters
    ----------
    kwargs
        device_name : str
            Emulator name.
        debug : bool
            False for headless mode.

    Returns
    -------
    Union
        Android emulator session.
        None
    """
    emulator_name = kwargs.get("device_name")
    debug = kwargs.get("debug")
    attached_devices = get_attached_android_devices()
    emulators_real_name = get_emulators_real_name(attached_devices)
    running_devices = attached_devices + emulators_real_name
    emulator_udid = {
        name_: id_ for name_, id_ in zip(emulators_real_name, attached_devices)
    }
    if emulator_name in running_devices:
        ARGUMENTS.appium_properties.mobile_udid = emulator_udid.get(
            emulator_name
        )
        return None
    if emulator_name not in get_available_emulators():
        print(r"\\          //  //\\  ||==|| ||\\  || == ||\\  || ====== ")
        print(r" \\  //\\  //  //==\\ ||==|| || \\ || || || \\ || ||  ===")
        print(r"  \\//  \\//  //    \\||   \\||  \\|| == ||  \\|| ||===||")
        print("==========================================================")
        print(f"The device/emulator {emulator_name} is not available.")
        print("==========================================================")
        return None
    print("===================================================")
    print(f"The device: {emulator_name} is not running")
    print("===================================================")
    command = ['emulator', '-avd', emulator_name]  # , '-no-snapshot']
    if name == 'nt':  # For window 10
        command = ["cmd", "/c"] + command
    if not debug:
        command += ['-noaudio', '-no-boot-anim', '-no-window']
    emulator_session = Popen(command, stdout=PIPE)
    print_progress_bar(
        wait_time=10,
        progress_status=f"Starting emulator {emulator_name}."
    )
    timeout = 10
    while True:
        if name == "posix":  # For MacOS 12
            fd = emulator_session.stdout.fileno()
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | O_NONBLOCK)
        line = emulator_session.stdout.readline()
        line_in_string = line.rstrip().decode('utf-8')
        print(line_in_string)
        if "emulator: INFO: boot completed" in line_in_string:
            break
        if not line_in_string:
            break
        if timeout <= 0:
            break
        sleep(1)
        timeout += -1
    attached_devices = get_attached_android_devices()
    emulators_real_name = get_emulators_real_name(attached_devices)
    emulator_udid = {
        name_: id_ for name_, id_ in zip(emulators_real_name, attached_devices)
    }
    ARGUMENTS.appium_properties.mobile_udid = emulator_udid.get(
        emulator_name)
    print("exit")
    return emulator_session


def free_port(port: int) -> None:
    """

    Parameters
    ----------
    port

    Returns
    -------

    """
    command = f"lsof -i :{port}"
    index = 9
    if name == 'nt':
        command = ["cmd", "/c", "netstat", "-ano", "|", "findstr", f"{port}"]
        index = 4
    c = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    standard_out, _ = c.communicate()
    output = standard_out.decode().strip().split(' ')
    while "" in output:
        output.remove("")
    try:
        pid = int(output[index])
        if name == 'nt':
            system(f'taskkill /f /im {pid}')
        else:
            kill(pid, SIGTERM)
    except IndexError:
        pass
    except TypeError as error:
        raise Exception(f"Could not kill process {output[9]}. {error}")
