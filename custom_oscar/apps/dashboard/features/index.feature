Feature: Dashboard Index Page
  As a designer and admin, I want to be able to view an overview or orders and see a chart of orders in the past 24 hours

  Scenario: Accessing the Dashboard as Non Designer
    Given I am logged in as <user>
    When I click the user Icon
    Then I can see the dropdown menu
    Then I should 'not' see the Dashboard link
    When I go to the url '/dashboard'
    Then I should not see the Dashboard page

  Scenario: Accessing the Dashboard
    Given I am logged in as <user>
    When I click on the user Icon
    Then I should see the Dashboard link
    When I click on 'Dashboard'
    Then I should see the Dashboard page

  Scenario: Designer Index Layout
    Given I am logged in as

  Scenario: Designer Index Shop Stats

  Scenario: Designer Index Orders - Last 24 Hours

  Scenario: Designer Index Order - All Time

  Scenario: Designer Index Catalogue