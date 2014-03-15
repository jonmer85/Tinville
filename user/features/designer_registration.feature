Feature: Designer Registration

  As a Designer
  I would like to register as a designer on Tinville
  So that I may use all of the features on Tinville, including opening up a Shop

  Scenario: Form entry
	When I register for a shop named "foo"
	Then I can visit my shop at "/foo/"

  Scenario: Shop name unavailable without applying for shop
    When I access the registration page
	Then I can't fill in the shop name
