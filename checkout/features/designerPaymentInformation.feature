# Created by mervetuccar at 11/28/14
Feature: Designer Payment Information

  As a designer
  I want to have a form that allows me to create payment account
  In order to receive payment upon a sale

  Scenario: Create Debit Payment Account
    Given: the designer is logged in
    When designer clicks on user icon
    And  drop down menu is displayed
    And  My Payment Info is displayed
    Then click on My Payment Info
    When payment info form is displayed
    And  the instruction is displayed
    #Enter your card information to get paid
    And  the name field is displayed
    And  the card number field is displayed
    And  the expiration date is displayed
    And  the CVC field is displayed
    And  the Submit button is displayed
    Then enter name as it seems on your debit card or bank account
    Then enter 16-digits card number
    Then enter expiration date in MM YY format
    Then enter CVC -the last three digits appears on the back of card
    When the format entered is correct
    Then submit the form

     Scenario: Edit a Payment Account
       Given: a payment account exists


       Scenario: Delete Payment Account
         Given: a payment account exists


