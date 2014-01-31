Feature: Shopper Registration

  As a shopper
  I would like to register with Tinville
  So that I may purchase apparel from designer shops

  Scenario: Login redirect
    When I register for a shopper account with email "foo@bar.com" and password "foobar"
    And I sign in
    Then I should be redirected to the home page

  @wip
  Scenario: Registration confirmation
    When I register for a shopper account with email "foo@bar.com" and password "foobar"
    Then I should see a confirmation notification prompting me to activate the account via email instructions
    And I should be redirected to the home page
