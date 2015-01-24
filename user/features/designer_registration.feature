Feature: Designer Registration

  As a Designer
  I would like to register as a designer on Tinville
  So that I may use all of the features on Tinville, including opening up a Shop

  Scenario: Form entry
	When I register for a shop named "foo"
	Then I can visit my shop at "foo"

  Scenario: Shop name unavailable without applying for shop
    When I access the registration page
	Then I can't fill in the shop name

  Scenario: I should not be able to register with a shopname that exists, no matter the capitalization
     When a shop named "foo" already exists
     And I try to register a shop named "foo"
     Then I should get an error that the shop already exists
     Or I try to register a shop named "FOO"
     Then I should get an error that the shop already exists
     Or I try to register a shop named "Foo"
     Then I should get an error that the shop already exists
     Or I try to register a shop named "fOO"
     Then I should get an error that the shop already exists

  Scenario Outline: I should not be able to register with a shopname that is a Tinville URL, no matter the capitalization
     When I try to register a shop named "<shopname>"
     Then I should get an error that the shop name is invalid
  Scenarios:
     | shopname |
     | admin    |
     | Admin    |
     | ADMIN    |
     | aDMIN    |

  Scenario: AW Defect 212 - Shop name URL should be case-insensitive
    When I register for a shop named "foo"
    Then I can visit my shop at "foo"
    And I can visit my shop at "FOO"
    And I can visit my shop at "Foo"

