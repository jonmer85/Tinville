Feature: Shopper Registration

  As a shopper
  I would like to register with Tinville
  So that I may purchase apparel from designer shops

  Scenario: Registration confirmation
    When I register for a shopper account with email "foo@bar.com" and password "foobar"
    Then I should be redirected to the home page
    And I should see a confirmation notification prompting me to activate the account via email instructions to "foo@bar.com"

  Scenario: Duplicate address
    When I register for a shopper account with email "foo@bar.com" and password "foobar"
    And I try to again register for a shopper account with email "Foo@bar.com" and password "foobar"
	Then I should get a validation error on email address

  Scenario: No initial validation
    When I access the registration page
	Then I should not see validation errors
