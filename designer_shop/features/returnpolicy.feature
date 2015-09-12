Feature: Designer Shop Return Policy Selection
  In order to add a return policy for the designer shop
  As a designer
  I want to have a text selection that allows me to add and modify text

  Scenario: Return Policy Editor
    Given the demo shop editor
    When the return policy edit button is pressed
    Then the return policy text field box is displayed
    And the return policy is submitted
    And the submit return policy button is displayed
    Then The return policy is saved