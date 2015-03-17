Feature: Designer Shop About Content Selection

  In order to add about content for the designer shop
  As a designer
  I want to have a text selection that allows me to add and modify text

  Scenario: About Box Editor
    Given the demo shop editor
    When the about edit button is pressed
    Then the about text field box is displayed
    And the submit about content button is displayed
    And the about content and image is submitted
    Then The about content is saved