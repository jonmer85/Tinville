Feature: Dashboard Index Page
  As a designer and admin, I want to be able to view an overview or orders and see a chart of orders in the past 24 hours

  Scenario: Accessing the Dashboard as Non Designer
    Given I am logged in as <user>
    When I click the user Icon
    Then I can see the dropdown menu
    Then I should 'not' see the Dashboard link

  Scenario: Designer Index Layout

  Scenario: Designer Index Shop Stats

  Scenario: Designer Index Orders - Last 24 Hours

  Scenario: Designer Index Order - All Time

  Scenario: Designer Index Catalogue