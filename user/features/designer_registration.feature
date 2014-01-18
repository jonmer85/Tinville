Feature: Designer Registration

  As a Designer
  I would like to register as a designer on Tinville
  So that I may use all of the features on Tinville, including opening up a Shop

  Scenario: Initial Information
	Given I access the URL '/register'
	Then I see information to register as a designer
	Or to register as a shopper



  Scenario: Shop Items
    Given I access the URL '/register'
	And 3 shop items
	When the shop is visited
	Then there should be 3 items displayed
	And every item should have a name
	And every item should have an image
	And every item should have a price

