Feature: Designer Shop

  In order to browse clothing
  As a customer
  I want to view a designer's shop

  Scenario: Page Elements
	Given a designer shop
	When the shop is visited
	Then the banner for the shop is displayed
	And the items for the shop are displayed
	And the Tinville header is displayed

  Scenario: Shop Items
	Given a designer shop
	And 3 shop items
	When the shop is visited
	Then there should be 3 items displayed
	And every item should have a name
	And every item should have an image
	And every item should have a price

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
    When I select the "filterGender" "Women"
    Then I should have "2" items in the demo shop

  Scenario: Type Filter Functionality
    Given the demo shop
    Given I have at least 3 items in the demo shop
    When I select the "filterType" "Boots"
    Then I should have "1" items in the demo shop

  Scenario: Gender Type Combo Filter Functionality
    Given the demo shop
    Given I have at least 3 items in the demo shop
    When I select the "filterGender" "Women"
    Then I should have "2" items in the demo shop
    When I select the "filterType" "Dresses"
    Then I should have "1" items in the demo shop



