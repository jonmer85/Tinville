Feature: Dashboard Index Page
  As a designer, I want to be able to view an overview or orders and see a chart of orders in the past 24 hours

  Scenario: Accessing the Dashboard as Non Designer
    Given I have some basic dashboard data
    Given I am logged in as <user>
    When I click the user Icon
    Then I can see the dropdown menu
    Then I should 'not' see the Dashboard link
    When I go to the url '/dashboard'
    Then I should not see the Dashboard page

  Scenario: Accessing the Dashboard
    Given I have some basic dashboard data
    Given I am logged in as demo@user.com
    When I click on the user Icon
    Then I should see the Dashboard link
    When I click on 'Dashboard'
    Then I should see the Dashboard page

  Scenario: Designer Index Menu
    Given I have some basic dashboard data
    Given I am on the dashboard index page
    Then I should see the 'dashboard nav menu'
    Then I should see the 'Dashboard' link
    Then I should see a 'Fulfilment' dropdown with the following options
      | Options    |
      | orders     |
      | statistics |

@wipjeff
  Scenario: Designer Index Shop Stats
    Given I have some basic dashboard data
    Given I am on the dashboard index page
    Then I should see the 'Your Shop Stats' table
    Then I should see my 'Total Orders'
    Then I should see my 'Total Products'
    Then I should see my 'New Customers - Last 24 Hours'
    Then I should see my 'Total Customers'

@wipjeff
  Scenario: Designer Index Alert
    Given I have some basic dashboard data
    Given I am on the dashboard index page
    Then I should see the 'Your Alerts' table
    Then I should see my 'Orders Ready to be Shipped'
    Then I should see my 'Setup Payment Info'
    Then I should see my 'Setup Shop Shipping Address'

@wipjeff
  Scenario: Designer Index Orders - Last 24 Hours
    Given I have some basic dashboard data
    Given I am on the dashboard index page
    Then I should see the 'Orders - Last 24 Hours' table
    Then I should see my 'Total orders'
    Then I should see my 'Total lines'
    Then I should see my 'Total revenue'
    Then I should see my 'Average order costs'

@wipjeff
  Scenario: Designer Index Order - All Time
    Given I have some basic dashboard data
    Given I am on the dashboard index page
    Then I should see the 'Orders - All Time' table
    Then I should see my 'Total orders'
    Then I should see my 'Total lines'
    Then I should see my 'Total revenue'
    Then I should see my 'Total open baskets'

@wipjeff
  Scenario: Designer Index Catalogue
    Given I have some basic dashboard data
    Given I am on the dashboard index page
    Then I should see the 'Catalogue' table
    Then I should see my 'Total products'