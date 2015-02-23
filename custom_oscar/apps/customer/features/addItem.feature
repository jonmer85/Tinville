# Created by mervetuccar at 12/25/14
Feature: Add item to the shopping bag

  As a customer
  I would like to add as many as items to my shopping bag
  So that I can checkout and pay for them


  @jon
  Scenario: Adding an item to the empty shopping bag
    Given Demo page
    When The shopping bag is empty
    Then I add an item to my shopping bag
    Then The bag icon should show the number of the item
    And  I click on the bag icon
    Then The checkout drop down is displayed
    And  I click on the checkout button
    Then The checkout form should be displayed

  @jon
  Scenario: Checkout page using arrows to control number of items
    Given Checkout page with an item to checkout
    When I increase the number of items by 2 using arrow
    Then The total sum should be 3
    And I decrease the number of items using arrow by 1
    Then The total sum should be 2


#  Scenario: Checkout
    #Given checkout page with 2 items
#    When I click on checkout button
#    Then The user login options page should be displayed
#    And I choose I am a returning customer, and my password is
#    And I click on continue
#    And I receive the warning messages
#    And I enter the correct info (demo@user.com - tinville)
#    And the address page is open
#    And I click on Ship to This address
#    Then The payment form should be displayed
#    And I enter correct form credentials
#    Then I click on Pay


  # Scenario: Deleting an item
  #  Given A shopping bag with 2 items
  # When I click on delete item button
  # Then The number of items should be 1
#    And I delete this item too
#    Then The the shopping bag should become empty
#    And I click on bag icon
#    Then It should say No Item in Your Bag
#    And I click on checkout button
#    Then The message should say 'You need to add some items to your basket to checkout'
#    And I click on continue shopping button
#    Then I go back to main page

#   Scenario: Trying to click on Add to Bag without choosing any item
#   Given Main Demo page with a shopping bag that is empty
#   Then I click on Add_to_Bag button
#   Then I receive the following warnings


  #Scenario: Checking out with empty basket 'You need to add some items to your basket to checkout'
  #Scenario: Check payment form


  #Scenario: Filling out address form
  #Scenario: Adding empty address
  #use the added address to checkout


  #This is not a valid local or international phone format.

  #Scenario: Attempting to Checkout when not logged in










