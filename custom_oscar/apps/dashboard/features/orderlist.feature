Feature: Dashboard Order List
  As a designer and admin, I want to be able to view a list of all my orders

@wipjeff
  Scenario: Accessing the Order List page
    Given I have some basic dashboard data
    Given I am on the dashboard index page
    Then I should see the 'Your Alerts' table
    Then I should see my 'Orders Ready to be Shipped'
    When I click on the 'orders' link
    Then I should see the Dashboard 'Order management' page
    Given I am on the dashboard index page
    Then I should see the 'Your Shop Stats' table
    Then I should see my 'Total Orders'
    When I click on the 'orders' link
    Then I should see the Dashboard 'Order management' page
    Given I am on the dashboard index page
    Then I should see the 'Orders - All Time' table
    When I click on the 'orders' link
    Then I should see the Dashboard 'Order management' page
    Given I am on the dashboard index page
    Then I should see the 'Orders - Last 24 Hours' table
    When I click on the 'orders' link
    Then I should see the Dashboard 'Order management' page


