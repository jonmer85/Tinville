Feature: Login

  As a Tinville User
  I would like to be able to login to Tinville
  So that I may have the site experienced personalized to me

  Scenario: Login redirect
    When I register for a shopper account with email "foo@bar.com" and password "foobar"
    And I sign in
    Then I should be redirected to the home page

  Scenario: Login error appears when no email is supplied
    When I access the home page
    When I fill in the login screen with email "" and password "test"
    Then I should see an error telling me that the email is required

  Scenario: Login with trailing spaces on the username
    When I register for a shopper account with email "foo@bar.com" and password "foobar"
    When I fill in the login screen with email "foo@bar.com " and password "foobar"
    Then I should be logged in
