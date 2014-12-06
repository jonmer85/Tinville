# Created by mervetuccar at 11/28/14
Feature: Designer Payment Information

  In order to receive payment upon a sale
  As a designer
  I want to have a form that allows me to create payment account



@wipmerve
  Scenario: Navigate to Designer Payment Form
    Given a designer is logged in
    When designer clicks on user icon
    And  drop down menu is displayed
    Then click on My Payment Info
    Then payment info form is displayed

@wipmerve
  Scenario: Payment Form Display
    Given the payment info form
    And  the 'full_legal_name' 'text' is displayed
    And  the 'card_number' 'text' is displayed
    And  the 'expiration_month' 'text' is displayed
    And  the 'expiration_year' 'text' is displayed
    And  the 'cvc' 'password' is displayed
    And  the 'payment-info' 'submit' is displayed

  Scenario: Validating Designer Debit Card Information
    Given the payment info form
    When enter 'full_legal_name' 'field'
    When enter 'card_number' 'text' card number
    When enter 'expiration_month' 'text' in MM  format
    When enter 'expiration_year' 'text' in YY format
    When enter 'cvc' 'password'
    When submit the form
    Then message should be pop up


  Scenario Outline: I should not be able to submit form

  When '<full_legal_name>' '<card_number>' '<expiration_month>' '<expiration_year>' '<cvc>' '<error>'
  Scenarios:
  | full_legal_name | card_number      | expiration_month | expiration_year | cvc | error              |
  | Merve T         | 4242424242424242 | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 4012888888881881 | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 5555555555554444 | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 5105105105105100 | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 378282246310005  | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 371449635398431  | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 6011111111111117 | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 6011000990139424 | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 30569309025904   | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 38520000023237   | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 3530111333300000 | 12               | 15              | 123 | "not a debit card" |
  | Merve T         | 3566002020360505 | 12               | 15              | 123 | "not a debit card" |



  Scenario Outline: Payment Info Form Validation
    Given the payment info form
    When I enter '<value>' in the '<field>'
    Then I should see an error that states '<error>'

  Scenarios:
    | value                 | field           | error                  |
    | -4000000000000002     | card number     | "card_declined"        |
    | 4242424242424241      | card number     | "incorrect_number"     |
    | 13                    | expiration_month| "invalid_expiry_month" |
    | 1970                  | expiration_year | "invalid_expiry_year"  |
    | 99                    | cvc             |  "invalid_cvc"         |


  Scenario Outline: Payment Info Stripe Validation
    Given the payment info form
    When I enter the following information
    | fieldname        |       value        |
    | full_legal_name  | <full_legal_name>  |
   Then I should see an error that states '<error>'



    #check both stripe validation and form validation for each debit card type Master,Visa, American Express etc.
   #success scenarios should be a separate one






