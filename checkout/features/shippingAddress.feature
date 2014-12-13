Feature: Shipping Address Verification

  In order to select a color for the designer shop
  As a designer
  I want to have a menu that allows me to choose a color for the shop

  In order to choose a destination for the package
  As a customer
  I want to have a form that presents all the address fields needed

  Scenario: Guest Customer
    Given: The demo shop
    When: the user is not signed in
    And an item is selected
    And the item is added to the basket
    And the user chooses to checkout
    Then the cart detail page is displayed
    And the users proceeds to checkout
    Then the customer type menu is displayed
    And the user chooses to checkout as guest
    Then the shipping address page is displayed
    And the first name field is displayed
    And the last name field is displayed
    And the first address line field is displayed
    And the second address line field is displayed
    And the third address line field is displayed
    And the city field is displayed
    And the state field is displayed
    And the zip field is displayed
    And the phone number field is displayed
    And the address is submitted
    Then the user fills out the shipping form
    And submits the shipping form
    Then the payment details page is displayed
    And the payment form is displayed
    Then the user fills out the payment form
    And submits the payment form
    Then the thank-you page is displayed

  Scenario: New Customer
    Given: The demo shop
    When: the user is not signed in
    And an item is selected
    And the item is added to the basket
    And the user chooses to checkout
    Then the cart detail page is displayed
    And the users proceeds to checkout
    Then the customer type menu is displayed
    And the user chooses new customer
    Then the first name field is displayed
    And the last name field is displayed
    And the first address line field is displayed
    And the second address line field is displayed
    And the third address line field is displayed
    And the city field is displayed
    And the state field is displayed
    And the zip field is displayed
    And the phone number field is displayed
    And the address is submitted
    Then the address for the order is stored

  Scenario: Regular Customer
    Given: The demo shop
    When the user is signed in
    And an item is added to the cart
    And the order proceeds to checkout
    And the shipping address form is displayed
    Then the first name field is displayed
    And the last name field is displayed
    And the first address line field is displayed
    And the second address line field is displayed
    And the third address line field is displayed
    And the city field is displayed
    And the state field is displayed
    And the zip field is displayed
    And the phone number field is displayed
    And the address is submitted
    Then the address for the order is stored