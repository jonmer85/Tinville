Feature: Beta Code

  As a New Designer
  I would like to register
  So that I may receive a beta code

  As a User
  I would like enter a beta key
  So that I may access a shop
  So that my cookie is set

  @yori
  Scenario: New Designer
    When I register for a shop named "BetaShop"
    Then My shop is given a beta code

  Scenario: User first access
    Given the beta shop
    Then the access code page is displayed
    And I enter the access code
    Then I should be redirected to the beta shop

  Scenario: Returning user
    Given the BetaShop
    Then I should be redirected to the beta shop