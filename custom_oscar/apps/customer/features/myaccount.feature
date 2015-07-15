Feature: My Account Page
  As a customer
  I would like the ability to manage information such as order history, my addresses, and email history
  So that I can go back and reference information and actions I have made on Tinville

  Scenario: My Account Page Link and General Layout
    Given I have some basic order data
    When I click the user Icon
    Then I should see the 'My Account' link
    When I click on 'My Account'
    Then I should see the 'My Account' page
    And the selected tab should be 'Order History'
    And I should see 3 top level orders

