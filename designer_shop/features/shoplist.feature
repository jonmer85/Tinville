Feature: Designer Registration

  As a Designer
  I would like to register as a designer on Tinville
  So that I may use all of the features on Tinville, including opening up a Shop

  Scenario: Add Shop and check if its in the list
	When I register for a shop named "foo"
	Then I can visit my shop at "/shoplist/"

