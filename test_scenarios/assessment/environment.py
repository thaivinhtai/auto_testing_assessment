#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from libs.automation_libs.common_funcs import \
    set_default_test_case_behavior, retry_on_failure, \
    mapping_browser_name_and_device_with_scenario_outline
from page_objects.web.home_page import HomePage


def before_feature(context, feature):
    for scenario_ in feature.scenarios:
        scenario_ = mapping_browser_name_and_device_with_scenario_outline(
            scenario_, HomePage().driver.browser, "demo")
        retry_on_failure(scenario_)


def before_scenario(context, scenario):
    context.name = scenario.name
    set_default_test_case_behavior(scenario=scenario,
                                   tsm_link_mapping=__TMS_LINK_MAPPING)


def after_feature(context, feature):
    HomePage().driver.close_browser()
    HomePage().driver.close_session()


__TMS_LINK_MAPPING = {
    'TC1': 'foo',
}
