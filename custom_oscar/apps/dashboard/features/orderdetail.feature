#TODO:Andy
Feature: Dashboard Order Detail
#  As a designer and admin, I want to be able to view the details about my orders, and buy shipping labels
#
#  Scenario: Order Detail Designer Elements
#    Given I have an order with at least '5' items
#    When I visit the orders page
#    And click on my order
#    Then I see my order
#    Then I can see the following Elements
#    | Selector |
#
#  Scenario: Order Detail Admin Elements
#    Given I have an order with at least '5' items
#    When I visit the orders page
#    And click on my order
#    Then I see my order
#    Then I can see the following Elements
#    | Selector |
#
#  Scenario: Designer Order detail Order Contents Tab
#    Given I am on the order details page
#    When I click on the Order Contents tab
#    Then I can see a table with the following columns
#    | ColumnName      |
#    | Select          |
#    | "Line ID"       |
#    | Product         |
#    | "Product Size"  |
#    | "Product Color" |
#    |"Price excl tax (before discounts)" |
#    | Actions                            |
#
#  Scenario: Designer Order Detail Shipping Tab
#
#  Scenario: Designer Order Detail Notes Tab
#
#  Scenario: Admin Order Detail Order Contents Tab
#    Given I am on the order details page
#    When I click on the Order Contents tab
#    Then I can see a table with the following columns
#    | ColumnName      |
#    | Select          |
#    | "Line ID"       |
#    | Product         |
#    | "Product Size"  |
#    | "Product Color" |
#    | UPC             |
#    | Status          |
#    | Supplier        |
#    | "Supplier SKU"  |
#    |"Price excl tax (before discounts)" |
#    | Actions                            |
#
#  Scenario: Admin Order Details Shipping Tab
#
#  Scenario: Admin Order Detail Notes Tab
#
#  Scenario: Admin Order Detail Payments Tab
#
#  Scenario: Admin Order Detail Offers Tab
#
#  Scenario: Admin Order Detail Emails Tab
#
#  Scenario: Ship It Modal Elements
#    Given I am on the order details page
#    When I click on the 'ShipIt' button
#    Then I should see the 'ShipIt' Modal
#    And I should see the following Elements
#    | Selector |
#
#  Scenario Outline: Fixed Rate Shipping and Buy
#    Given I am on the order details page
#    When I select '<selected_item_count>' with '<amount_per_item>' items each
#    And I click on the 'Ship It!' button
#    Then I should see the 'ShipIt' Modal
#    When I select the shipping option '<shipping_option>'
#    And I click on the 'Confirm Shipping Option' button
#    Then my shipping option is <result>
#
#  Scenarios:
#    | selected_item_count | amount_per_item | shipping_option | result |
#    | 0                   | 0               |                 | "You must select some lines to act on" |
#
#  Scenario Outline:
#
