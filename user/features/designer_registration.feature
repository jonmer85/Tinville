Feature: Designer Registration

  As a Designer
  I would like to register as a designer on Tinville
  So that I may use all of the features on Tinville, including opening up a Shop

  Scenario: Initial Information
	Given I access the registration page
	Then I see information to register as a designer
	Or to register as a shopper

  Scenario: Collapsed forms
    Given I access the registration page
    Then all registration forms are initially collapsed
