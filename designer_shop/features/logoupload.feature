Feature: Designer Shop Logo Upload Selection

  In order to upload a logo image for the designer shop
  As a designer
  I want to have a file selection that allows me to choose the image

  @tommy
  Scenario: Logo Menu
    Given the demo shop editor
    When the logo tab is selected
    Then the logo file upload is displayed
    And the submit logo button is displayed
    And a logo is submitted
    The selected logo file is saved