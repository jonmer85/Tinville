Feature: Dashboard Order List
  As a designer and admin, I want to be able to view a list of all my orders

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

  Scenario: Order Filter
    Given I have some basic dashboard data
    Given I am on the dashboard order list page
    When I click on the 'All Orders' filter
    Then I should see '3' orders
    When I click on the 'Ready for Shipment' filter
    Then I should see '2' orders
    
  Scenario: Order Columns
    Given I have some basic dashboard data
    Given I am on the dashboard order list page
    Then I should see the following columns
    | Column             |
    | Order number       |
    | "Total inc tax"    |
    | "Number of items"  |
    | Status             |
    | Customer           |
    | "Shipping address" |
    | "Date of purchase" |

#  Scenario: Order view button text
#    Given I have some basic dashboard data
#    Given I am on the dashboard order list page
#    When I click on the 'All Orders' filter
#    Then I should see '2' orders with a 'Ship' button
#    And I should see '1' orders with a 'View' button

#  Scenario: Order Search
#    Given I have some basic dashboard data
#    Given I am on the dashboard order list page
#    When I search for order '1-100002'
#    Then I should see the Dashboard 'Order #1-100002' page

