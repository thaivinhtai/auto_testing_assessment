#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Steps execution
"""

from behave import given, when, then, step
from selenium.common.exceptions import InvalidSwitchToTargetException, \
    NoSuchFrameException, NoSuchWindowException

from page_objects.web import HomePage, LoginPage, SideMenu, ProfileMenu, \
    DevicesPage
from page_objects.android import WelcomeScreen, ActivationScreen, \
    LoginScreen, OTPScreen, FooterMenu, ChatScreen, ContactProfileScreen, \
    ContactScreen
from resource.common_variables import USER_1, USER_2, USER_1_PASS, \
    USER_2_PASS, DEFAULT_OTP, DEFAULT_COMPANY, TEST_MESSAGE, REPLY_TEST_MESSAGE


@given("User 1 logs in to the Web in order to obtain the QR code needed"
       " to access the Mobile application")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Access to web page and login
    HomePage().access_home_page_url()
    LoginPage().log_in(company=DEFAULT_COMPANY, otp=DEFAULT_OTP,
                       username=USER_1, password=USER_2_PASS)

    # Open userprofile from side menu
    SideMenu().open_to_user_profile()
    # Click on Devices tab to open Devices page
    ProfileMenu().open_devices_page()

    # Get activation code
    DevicesPage().click_on_link_device()
    context.activation_code = DevicesPage().get_activation_code()


@when("User 1 logs in to the Mobile application")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Open app and skip the Welcome Screens.
    WelcomeScreen().open_app()
    WelcomeScreen().click_on_skip_button()

    # Enter activation code.
    ActivationScreen().enter_activation_code(context.activation_code)
    # Enter password and login.
    LoginScreen().log_in(USER_1_PASS)

    # Enter OTP.
    OTPScreen().enter_otp(otp_value=DEFAULT_OTP)


@step("User 1 sends a message to User 2 and replies to that message itself")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    # Navigate to Contact Screen
    FooterMenu().click_on_contact_tab()

    # Switch to Team Tab and search for User 2
    ContactScreen().switch_to_tab_team()
    ContactScreen().click_on_first_team_searching_result(keyword=USER_2)

    # Click on Chats button of User 2 profile screen
    ContactProfileScreen().click_on_chat()

    # Send message to User 2
    ChatScreen().send_message(message=TEST_MESSAGE)
    return True


@then("User 2 should see the reply message from User 1 on the Web")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    return True