Feature: Designer Shop Banner Upload Selection

  In order to upload a banner image for the designer shop
  As a designer
  I want to have a file selection that allows me to choose the banner

  Scenario: Banner Menu
    Given the demo shop editor
    When the banner button is pressed
    Then the banner file upload is displayed
    And the submit banner button is displayed
    And a banner is submitted
    Then The selected banner file is saved