Feature: Zendesk

  Zendesk should be visible

  @zendesk
  Scenario: Zendesk on demo shop page
    Given the demo shop
    Then the zendesk icon should exist