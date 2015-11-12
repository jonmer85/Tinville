Feature: Register with Social Media credentials

  @jon
  Scenario: Register with Facebook
    Given Tinville has the proper Social account connection
    And I access the home page
    When I register as a Facebook user
    And I should have a pop-up message saying I have signed in with "qbarld_laverdetstein_1446602162@tfbnw.net"
    And I should have my email visible "qbarld_laverdetstein_1446602162@tfbnw.net"

  @jon
  Scenario: Register with Instagram
    Given Tinville has the proper Social account connection
    And I access the home page
    When I click the Instagram signin link I should get to the signin page


#  Scenario: Register with Facebook but email already exists...
#
#  Scenario: Register with Instagram but email already exists
#
#  Scenario: Sign In with Facebook when a user was registered through Tinville directly

