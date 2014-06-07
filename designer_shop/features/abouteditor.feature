Feature: Designer Shop About Content Selection

  In order to add about content for the designer shop
  As a designer
  I want to have a text selection that allows me to add and modify text

  @tommy
  Scenario: About Box Editor
    Given a shop editor
    When the about tab is selected
    Then the about text field box is displayed
    And the submit about content button is displayed
    And the about content is submitted
  The about content is saved