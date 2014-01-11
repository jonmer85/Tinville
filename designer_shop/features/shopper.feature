Feature: Designer Shop

  In order to browse clothing
  As a customer
  I want to view a designer's shop

  Scenario: Page Elements
	Given a designer shop
	When the shop is visited
	Then the banner for the shop is displayed
	And the logo for the shop is displayed
	And the items for the shop are displayed

  Scenario: Shop Items
    Given a designer shop
	And 3 shop items
	When the shop is visited
	Then there should be 3 items displayed
	And every item should have a name
	And every item should have an image
	And every item should have a price

