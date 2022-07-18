#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Custom logging module.
"""

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from datetime import datetime
from allure import attach, attachment_type

from .runtime_variable_namespace import RuntimeVariable
from .args_parser import ARGUMENTS


class CustomLogger:
    """Custom logger.

    This class is a custom logger for the framework. Via implement module
    logger of robot.api library, this class provides logging for multiple
    levels (info, debug, warn, error).

    Parameters
    ----------
    current_test_name : str
        Current executing test case's name.

    Attributes
    ----------
    __current_test_name : str
        Current executing test case's name.
    _logging : robot.api.logger
        Robot logger instance.

    Methods
    -------
    __log_to_console(self, level: str, message: str) -> None
        Private method, print log to console.

    debug(self, message: str) -> None:
        Call Logger at Debug level.

    info(self, message: str, timestamp=True) -> None:
        Call Logger at Info level.

    warn(self, message: str) -> None:
        Call Logger at Warn level.

    error(self, message: str) -> None:
        Call Logger at Error level.
    """

    def __init__(self, current_test_name: str = ""):
        """Constructor."""
        self.__current_test_name = current_test_name
        self._logging = logger

    def __log_to_console(self, level: str, message: str,
                         timestamp: bool = True) -> None:
        """Log to console.

        This method print log to console.

        Parameters
        ----------
        level : str
            Level of log.
        message : str
            Content to be logged.
        timestamp : bool
            True if time stamp, False if none.

        Returns
        -------
        None
        """
        current = datetime.now().strftime("%Y-%m-%d %H-%M-%S.%f")
        beginning_space = "        " if ARGUMENTS.run_behave else  ""
        time_stamp_prefix = beginning_space + current + ' - ' + level + ' - '
        if not timestamp:
            time_stamp_prefix = ''
        self._logging.console(time_stamp_prefix + message)
        execution_log = open(
            f'{RuntimeVariable.CURRENT_LOG_DIR}/execution.log', 'a+'
        )
        execution_log.write(time_stamp_prefix + message + '\n')
        if ARGUMENTS.run_behave and ARGUMENTS.debug:
            attach(time_stamp_prefix + message,
                   attachment_type=attachment_type.TEXT)

    def debug(self, message: str) -> None:
        """Debug.

        This method logs at Debug level.

        Parameters
        ----------
        message : str
            Content to be logged.

        Returns
        -------
        None
        """
        self._logging.debug(message)
        self.__log_to_console(level='DEBUG', message=message)

    def info(self, message: str, timestamp: bool = True, **kwargs) -> None:
        """Info.

        This method logs at Info level.

        Parameters
        ----------
        message : str
            Content to be logged.
        timestamp : bool
            True -> add timestamp to message.

        Returns
        -------
        None
        """
        self._logging.info(message, **kwargs)
        self.__log_to_console(level='INFO', message=message,
                              timestamp=timestamp)

    def warn(self, message: str) -> None:
        """Warn.

        This method logs at Warn level.

        Parameters
        ----------
        message : str
            Content to be logged.

        Returns
        -------
        None
        """
        self._logging.warn(message)
        self.__log_to_console(level='WARN', message=message)

    def error(self, message: str) -> None:
        """Error.

        This method logs at Error level.

        Parameters
        ----------
        message : str
            Content tobe logged.

        Returns
        -------
        None
        """
        self._logging.error(message)
        self.__log_to_console(level='ERROR', message=message)

    @property
    def current_test_name(self) -> str:
        """Get current test name.

        Returns
        -------
        str
        """
        return self.__current_test_name


LOGGER = CustomLogger() if ARGUMENTS.run_behave \
    else CustomLogger(BuiltIn().get_variable_value("${TEST_NAME}"))
