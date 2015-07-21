Feature: Filter Session State
  As a user, I want the drop downs and filter to remember their state during a session
  Scenario: Drop Down on the shop page
    Given the shop page
    When I click on the filter dropdowns
    And I refresh the page
    Then the filter should remain in the same state