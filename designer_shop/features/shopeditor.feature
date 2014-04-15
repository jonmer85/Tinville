Feature: Shop Editor Shell

@wip
  Scenario: Shop Editor Shell non-XS loaded
    Given the demo shop
    The designer can open a shop editor
    There should be 2 icons displayed for control
    And a panel for options
    And a panel with the content for the selected panel
    And a global submit button
    And the shop editor is 35% of the window size by default
@wip
  Scenario: Shop Editor Shell non-XS size control
    Given a shop editor
    There should be 2 icons displayed for size control
    Then selecting the down arrow should minimize the shop
    And selecting the up arrow should expand the shop again
    And selecting the double arrows should increase the size of the shop to 75% of window size
    And selecting the double inward arrows should decrease the size of the shop to 35% of window size again