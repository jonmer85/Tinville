Feature: Designer Shop

  In order to browse clothing
  As a customer
  I want to view a designer's shop

  Scenario: Banner
    Given a designer shop
	When the shop is visited
	Then the banner for the shop is displayed
