#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module handles switching test suite and get data.

    Private function in this module:

        +   __get_robot_vars(**kwargs) -> list
                Collects input of user and return a list that contains flags
                of robot to assign value for variables in robot test cases.

    Public function:

        +   switch_to_tds(**kwargs) -> list
                Collects all arguments as a list based on user's input.
"""

from .args_parser import ARGUMENTS


def switch_to_tds(**kwargs) -> list:
    """Switch to Test Domain Specification.

    This function collects all arguments as a list based on user's input.

    Parameters
    ----------
    kwargs : dict

    Returns
    -------
    list
        List of all arguments that will be input of robot subprocess.
    """
    test_module = str(kwargs.get('module'))
    test_design = str(kwargs.get('test_design'))
    temp_tags = kwargs.get('tags')
    levels = kwargs.get("levels")
    mode = str(kwargs.get("mode")).lower()
    browser = kwargs.get('browser')
    phone_simulator = kwargs.get('phone_simulator')
    app_package = kwargs.get('app_package')
    app = kwargs.get('app')
    mobile_platform = kwargs.get('mobile_platform')
    mobile_platform_ver = kwargs.get('mobile_platform_ver')
    version = str(kwargs.get('version'))
    skip_check_version = True
    if version.lower() != 'all':
        version = Version(str(kwargs.get('version')))
        skip_check_version = False
    run_job = kwargs.get('run_job')
    debug = kwargs.get('debug')

    list_test_cases, test_cases_file =\
        get_list_test_cases_and_feature_file(module_name=test_module,
                                             test_design=test_design)

    # Prepare tags list
    tags = []
    if temp_tags:
        for tag in temp_tags:
            # tags.append('-i')
            tags.append(tag)

    # Get value for robot vars
    robot_vars = None
    if not ARGUMENTS.run_behave:
        robot_vars = __get_robot_vars(test_module=test_module, browser=browser,
                                      phone_simulator=phone_simulator,
                                      mobile_platform=mobile_platform, app=app,
                                      mobile_platform_ver=mobile_platform_ver,
                                      app_package=app_package, run_job=run_job)

    executed_test_cases = list()

    tags_by_test_case = None
    if not ARGUMENTS.run_behave:
        tags_by_test_case = get_tags(robot_suite=test_cases_file)
    else:
        tags_by_test_case = \
            get_behave_testcase_documentation_and_tags(
                feature_file=test_cases_file
            )

    # Handle version, if test case has version specification that does not
    # match, ignore it.
    for test_case in list_test_cases:
        if skip_check_version:
            pass
        elif version < Version(get_test_metadata(test_name=test_case,
                                                 name='min_version',
                               tags=tags_by_test_case[test_case])):
            continue
        elif version >=\
                Version(get_test_metadata(test_name=test_case,
                                          name='min_version',
                                          tags=tags_by_test_case[test_case]))\
                and\
                get_test_metadata(
                    test_name=test_case, name='max_version',
                    tags=tags_by_test_case[test_case]).lower() == "none":
            pass
        elif version >\
                Version(get_test_metadata(test_name=test_case,
                                          name='max_version',
                                          tags=tags_by_test_case[test_case])):
            continue
        if get_test_metadata(test_name=test_case,
                             name='level',
                             tags=tags_by_test_case[test_case]).lower()\
                not in levels and levels != ['all']:
            continue
        if get_test_metadata(test_name=test_case,
                             name='mode',
                             tags=tags_by_test_case[test_case]).lower()\
                != mode.lower() and mode.lower() != 'all':
            continue
        if not tags:
            pass
        elif not bool(set(tags) & set(tags_by_test_case[test_case])):
            continue
        executed_test_cases.append(test_case)

    if executed_test_cases:
        return [
            test_cases_file,
            {
                'test': executed_test_cases,
                'variable': robot_vars,
                'include': tags
            }
        ]
    if debug:
        print("==============================================================")
        print("There is no scenario to execute in file:", test_cases_file)
        print("--------------------")
        print("List test cases that can not be executed are: ")
        print("--------------------")
        print(*list_test_cases, sep="\n")
        print("==============================================================")
    return []
