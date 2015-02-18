Feature: Under construction
  As a Designer
  I would like to access my shop
  Whether it is approved or not

  As a User
  I would only have access to the shop if the shop is approved

  Scenario: Designer accessing not approved shop
	When I register for a shop named "foo"
    And I sign in
    And their shop is not approved
	Then I can visit my new shop at "foo"

  Scenario: User accessing not approved shop
    When the shop is not approved
    And I visit my new shop at "Demo"
    Then I should be redirected to the under construction page

  Scenario: User accessing approved shop
    When the shop is approved
    Then I can visit the demo shop