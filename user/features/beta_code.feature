Feature: Beta Code

  As a Designer
  I would like to register a shop
  So that I may receive a beta code

  As a User
  I would like enter a beta key
  So that I may access a shop
  So that my cookie is set

  @yori
  Scenario: Form entry and user first and second access
    When I register for a shop named "BetaShop"
    And I can visit my shop at "/BetaShop/"
    Given the beta shop
    Then the access code page is displayed
    And I enter the access code
    Then I should be redirected to the beta shop
    Given the beta shop
    Then I should be redirected to the beta shop