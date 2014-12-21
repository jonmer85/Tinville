# Created by mervetuccar at 11/28/14
Feature: Designer Payment Information

  In order to receive payment upon a sale
  As a designer
  I want to have a form that allows me to create payment account



  Scenario: Navigate to Designer Payment Form
    Given a designer is logged in
    When designer clicks on user icon
    And  drop down menu is displayed
    Then click on My Payment Info
    Then payment info form is displayed

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

  Scenario Outline: I should not be able to receive a success message
    Given the payment info form
    When  I fill the form with
    | full_legal_name | card_number      | expiration_month | expiration_year | cvc |
    | <full_legal_name>| <card_number>   |<expiration_month>|<expiration_year>|<cvc>|
    And I submit the form
    Then I should see an error that states '<error>'

  Scenarios:
  | full_legal_name | card_number      | expiration_month | expiration_year | cvc | error                                                             |
  | Merve T         | 4242424242424242 | 12               | 15              | 123 | "This card doesn't appear to be a debit card."                    |
  | Merve T         | 4012888888881881 | 12               | 15              | 123 | "This card doesn't appear to be a debit card."                    |
  | Merve T         | 5555555555554444 | 12               | 15              | 123 | "This card doesn't appear to be a debit card."                    |
  | Merve T         | 5105105105105100 | 12               | 15              | 123 | "This card appears to be a prepaid debit card."                   |
  | Merve T         | 378282246310005  | 12               | 15              | 123 | "This card doesn't appear to be a Visa or MasterCard debit card." |
  | Merve T         | 371449635398431  | 12               | 15              | 123 | "This card doesn't appear to be a Visa or MasterCard debit card." |
  | Merve T         | 6011111111111117 | 12               | 15              | 123 | "This card doesn't appear to be a Visa or MasterCard debit card." |
  | Merve T         | 6011000990139424 | 12               | 15              | 123 | "This card doesn't appear to be a Visa or MasterCard debit card." |
  | Merve T         | 30569309025904   | 12               | 15              | 123 | "This card doesn't appear to be a US debit card."                 |
  | Merve T         | 38520000023237   | 12               | 15              | 123 | "This card doesn't appear to be a US debit card."                 |
  | Merve T         | 3530111333300000 | 12               | 15              | 123 | "This card doesn't appear to be a US debit card."                 |
  | Merve T         | 3566002020360505 | 12               | 15              | 123 | "This card doesn't appear to be a US debit card."                 |
  | Merve           | 4000056655665556 | 12               | 15              | 123 | "Name must contain first name and last name."                     |
  | Merve T         | -4000000000000002| 12               | 15              | 123 | "This card doesn't appear to be a debit card."                    |
  | Merve T         | 4242424242424241 | 12               | 15              | 123 | "This card doesn't appear to be a debit card."                    |

  Scenario Outline: Expiration month and year validation
    Given the payment info form
    When I fill the form with
    | full_legal_name | card_number      | expiration_month | expiration_year | cvc |
    | <full_legal_name>| <card_number>   |<expiration_month>|<expiration_year>|<cvc>|
    Then I should see the following '<error>' immediately

  Scenarios:
    | full_legal_name | card_number      | expiration_month | expiration_year | cvc | error                        |
    | Merve T         | 4000056655665556 | 13               | 15              | 123 | Invalid card expiration date |
    | Merve T         | 4000056655665556 | 12               | 70              | 123 | Invalid card expiration date |

  Scenario Outline: CVC error check
    Given the payment info form
    When I fill the form with
    | full_legal_name | card_number      | expiration_month | expiration_year | cvc |
    | <full_legal_name>| <card_number>   |<expiration_month>|<expiration_year>|<cvc>|
    And I submit the form
    Then I should see the following '<error>' immediately

  Scenarios:
    | full_legal_name | card_number      | expiration_month | expiration_year | cvc | error                          |
    | Merve T         | 4000056655665556 | 13               | 15              | 99  | Invalid card verification code |


  Scenario Outline: Payment Info Success
    Given the payment info form
    When I enter the following information
    When I fill the form with
    | full_legal_name | card_number      | expiration_month | expiration_year | cvc |
    | <full_legal_name>| <card_number>   |<expiration_month>|<expiration_year>|<cvc>|
    And I submit the form
    Then I should see success message that states '<success>'

  Scenarios:
  |full_legal_name  | card_number       | expiration_month | expiration_year | cvc  | success                                         |
  | Merve T         | 4000056655665556  | 12               | 15              | 123  | "You have successfully added your payment info" |
  | Merve T         | 5200828282828210  | 12               | 15              | 123  | "You have successfully added your payment info" |


@wipmerve
  Scenario Outline: Payment Info wrong month,year,cvc failure
   Given the payment info form
   When I enter the following information with wrong month,year,cvc information
   | full_legal_name | card_number      | expiration_month | expiration_year | cvc |
   | <full_legal_name>| <card_number>   |<expiration_month>|<expiration_year>|<cvc>|
   Then I should see the following '<failure>' messages

  Scenarios:
    |full_legal_name  | card_number       | expiration_month | expiration_year  | cvc  | failure                                                       |
    | X Y             | 4000056655665556  | 12               | demo@user.com    | 123  | "parameter should be an integer (instead, is demo@user.com)." |
    | X Y             | 4000056655665556  | 12               | 99               | 123  | "Your card's expiration year is invalid."                     |
    | X Y             | 4000056655665556  | 65               | 15               | 123  | "Your card's expiration month is invalid."                    |






#check both stripe validation and form validation for each debit card type Master,Visa, American Express etc.
#success scenarios should be a separate one






