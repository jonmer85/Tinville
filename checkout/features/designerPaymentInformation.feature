# Created by mervetuccar at 11/28/14
Feature: Designer Payment Information

  As a designer
  I want to have a form that allows me to create payment account
  In order to receive payment upon a sale

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
    Given the payment info form displayed
    When enter 'full_legal_name' 'field'
    When enter 'card_number' 'text' card number
    When enter 'expiration_month' 'text' in MM  format
    When enter 'expiration_year' 'text' in YY format
    When enter 'cvc' 'password'
    When submit the form
    Then message should be pop up

  Scenario Outline: Payment Info Form Validation
    Given the payment info form
    When I enter '<value>' in the '<field>'
    Then I should see an error that states '<error>'

  Scenarios:
    | value | field | error |
    | 1     | expiration_month| "invalid expiration month" |
    | 1     | expiration_year | "invalid expiration year"  |
    | 1     | cvc             |  "invalid cvc"             |


  Scenario Outline: Payment Info Stripe Validation
    Given the payment info form
    When I enter the following information
    | fieldname        |       value        |
    | full_legal_name  | <full_legal_name>  |
   Then I should see an error that states '<error>'

  Scenarios:
  | full_legal_name | card_number      | expiration_month | expiration_year | cvc | error              |
  | "Jeff Bowman"   | 4242424242424242 | 12               | 13              | 123 | "not a debit card" |

    #check both stripe validation and form validation for each debit card type Master,Visa, American Express etc.
   #success scenarios should be a separate one






