# Created by mervetuccar at 12/25/14
Feature: Add item to the shopping bag

  As a customer
  I would like to add as many as items to my shopping bag
  So that I can checkout and pay for them

  Scenario: Adding an item to the empty shopping bag
    Given Demo page
    When The shopping bag is empty
    Then I add an item to my shopping bag
    Then The bag icon should show the number of the item
    And  I click on the bag icon
    Then The checkout drop down is displayedF
    And  I click on the checkout button
    Then The checkout form should be displayed

  Scenario: Guest Checkout
    Given Demo page
    Then I add an item to my shopping bag
    And  I click on the bag icon
    Then The checkout drop down is displayed
    And  I click on the checkout button
    When I click on checkout button
    And I continue as guest
    Then I add a valid address
    Then I enter a valid payment
    Then the thank you page is displayed

  Scenario: Registered User Checkout
    Given Demo page
    Then I add an item to my shopping bag
    And  I click on the bag icon
    Then The checkout drop down is displayed
    And  I click on the checkout button
    When I click on checkout button
    And I sign in
    Then I add a valid address
    Then I enter a valid payment
    Then the thank you page is displayed

  Scenario: User Registers During Checkout
    Given Demo page
    Then I add an item to my shopping bag
    And  I click on the bag icon
    Then The checkout drop down is displayed
    And  I click on the checkout button
    When I click on checkout button
    And I choose to register
    Then I add my address
    Then I enter a valid payment
    Then the thank you page is displayed

  Scenario: Signed In User Checks Out
    Given Demo page
    When a registered user logs in with email "demo@user.com " and password "tinville"
    Then I add an item to my shopping bag
    And  I click on the bag icon
    Then The checkout drop down is displayed
    And  I click on the checkout button
    When I click on checkout button
    Then I add my address
    Then I enter a valid payment
    Then the thank you page is displayed