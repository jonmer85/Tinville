Feature: Shopping Cart

  As a shopper, I would like to manipulate my shopping cart.

@desktopCart
Scenario: Open and Close Desktop Shopping Cart
  Given a desktop shopper
  When I click the Desktop Shopping cart button
  Then the Shopping cart opens
  When I click the Desktop Shopping cart button
  Then the Shopping cart closes

@desktopCartAdd
Scenario: Add and Remove Cart Item
  Given a desktop shopper
  When I add an item to my cart
  When I click the Desktop Shopping cart button
  Then the item is added to my cart
  When I remove an item from my cart
  Then the item is removed from my cart


@mobileCart
Scenario: Open and Close Mobile Shopping Cart
  Given a mobile shopper
  When I click the Mobile Shopping cart button
  Then the Shopping cart opens
  When I click the Mobile Shopping cart button
  Then the Shopping cart closes

@mobileCartMenu
Scenario: Open Mobile Shopping Cart and Close via Menu
  Given a mobile shopper
  When I click the Mobile Shopping cart button
  Then the Shopping cart opens
  When I click the Menu button
  Then the Shopping cart closes