Feature: Designer Shop

  In order to browse clothing
  As a customer
  I want to view a designer's shop

  Scenario: Shop filters
    Given the demo shop
    Given I have at least 3 items in the demo shop
    Then I should see the following filters
      | FilterName     | DefaultValue     |
      | filterGender   | "View All"       |
      | filterType     | "View All Types" |
      | filterSort     | "No Sorting"     |

  Scenario: Gender Filter Functionality
    Given the demo shop
    Given I have at least 3 items in the demo shop
    When I select the "filterGender" "Men"
    Then I should have "2" items in the demo shop


  Scenario: Type Filter Functionality
    Given the demo shop
    Given I have at least 3 items in the demo shop
    When I select the "filterType" "Boots"
    Then I should have "1" items in the demo shop

  Scenario: Gender Type Combo Filter Functionality
    Given the demo shop
    Given I have at least 3 items in the demo shop
    When I select the "filterGender" "Men"
    Then I should have "2" items in the demo shop
    When I select the "filterType" "Jackets"
    Then I should have "1" items in the demo shop
    When I select the "filterGender" "View All"
    Then I should have "2" items in the demo shop

