Feature: Shop Editor Shell

  Scenario: Shop Editor Shell non-XS loaded
    Given the demo shop
    The designer can open a shop editor
    There should be 1 icon displayed for control
    And a panel for options
    And a panel with the panel
    And a global submit button
    And the shop editor is 85% of the window size by default

  Scenario: Shop Editor Shell non-XS size control
    Given a shop editor
    There should be 1 icon displayed for size control
    Then selecting the down arrow should minimize the shop editor
    And selecting the up arrow should expand the shop editor again

@wip
  Scenario: Shop Editor Shell XS loaded

@wip
  Scenario: Shop Editor Shell XS size control