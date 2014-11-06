Feature: Shopping Cart

  As a shopper, I would like to manipulate my shopping cart.

Scenario: Add and Remove Cart Item
  Given a desktop shopper
  When I add an item to my cart
  When I click the Desktop Shopping cart button
  Then the item is added to my cart
  When I remove an item from my cart
  Then the item is removed from my cart

Scenario: Add, Sign in and Remove Cart Item
  Given a desktop shopper
  When I add an item to my cart
  Then the item is added to my cart
  When I register for a shopper account
  And I sign in
  Then add another item is still in my cart
  When I log in or out
  Then all items are removed from my cart

