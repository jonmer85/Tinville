Feature: Under construction
  As a Designer
  I would like to access my shop
  Whether it is approved or not

  As a User
  I would only have access to the shop if the shop is approved

  @yori
  Scenario: Designer accessing not approved shop
	When I register for a shop named "foo"
    And the shop is not approved
	Then I can visit my shop at "foo"

  @yori
  Scenario: User accessing not approved shop
    Given the demo shop
    And the shop is not approved
    Then I should be redirected to the under construction page

  @yori
  Scenario: User accessing approved shop
    Given the demo shop
    And the shop is approved
    Then I can visit my shop at "foo"