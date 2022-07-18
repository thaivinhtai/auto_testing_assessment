# Created by thaivinhtai at 18/07/2022
@allure.epic:Automation
Feature: Assessment
  """
  Feature description here
  """

  Scenario Outline: TC1 - User 1 replies to a message on <mobile>, then User 2 checks the message on <browser>
    Given User 1 logs in to the Web in order to obtain the QR code needed to access the Mobile application
    When User 1 logs in to the Mobile application
      And User 1 sends a message to User 2 and replies to that message itself
    Then User 2 should see the reply message from User 1 on the Web

    Examples:
      | mobile  | browser |
      |    .    |     .   |
