Feature: Designer Shop Banner Upload Selection

  In order to upload a banner image for the designer shop
  As a designer
  I want to have a file selection that allows me to choose the banner

  @tommy
  Scenario: Banner Menu
    Given a shop editor
    When the lobannergo tab is selected
    Then the banner file upload is displayed
    And the create button is displayed
    And a banner is submitted
  The selected banner is applied to the shop