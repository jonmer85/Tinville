Feature: Dashboard Index Page
  As a designer, I want to be able to view an overview or orders and see a chart of orders in the past 24 hours

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

  Scenario: Designer Index Menu
    Given I am on the dashboard index page
    Then I should see the dashboard nav menu
    Then I should see a Fulfilment dropdown with the following options
      | Options    |
      | orders     |
      | statistics |

  Scenario: Designer Index Shop Stats
    Given I am on the dashboard index page
    Then I should see the Shop Stats
    Then I should see my Total Orders
    Then I should see my Total Products
    Then I should see my New Customers - Last 24 Hours
    Then I should see my Total Customers

  Scenario: Designer Index Alerts
    Given I am on the dashboard index page
    Then I should see the Your Alerts
    Then I should see Orders Readt to be Shipped
    Then I should see Setup Payment Info
    Then I should see Setup Shop Shipping Address

  Scenario: Designer Index Orders - Last 24 Hours
    Given I am on the dashboard index page
    Then I should see the Orders - Last 24 Hours
    Then I should see my Total orders
    Then I should see my Total lines
    Then I should see my Total revenue
    Then I should see my Average order costs

  Scenario: Designer Index Order - All Time
    Given I am on the dashboard index page
    Then I should see the Orders - All Time
    Then I should see my Total orders
    Then I should see my Total lines
    Then I should see my Total revenue
    Then I should see my Total open baskets

  Scenario: Designer Index Catalogue
    Given I am on the dashboard index page
    Then I should see the Catalogue
    Then I should see my Total products