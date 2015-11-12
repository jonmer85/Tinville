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
    And  the 'recipient_type' select is displayed
    And  the 'full_legal_name' 'text' is displayed
    And  the 'tax_id' 'text' is displayed
    And  the 'card_number' 'text' is displayed
    And  the 'expiration_date' 'text' is displayed
    And  the 'cvc' 'password' is displayed
    And  the 'payment-info' 'submit' is displayed

  Scenario Outline: I should not be able to receive a success message
    Given the payment info form
    When  I fill the form with
    | full_legal_name  | card_number     | tax_id   | expiration_date | cvc |
    | <full_legal_name>| <card_number>   | <tax_id> |<expiration_date>|<cvc>|
    And I submit the form
    Then I should see an error that states '<error>'

  Scenarios:
  | full_legal_name | card_number      | tax_id          | expiration_date | cvc | error                                                             |
  | Merve T         | 4242424242424242 | 000000000       | 1220            | 123 | "This card doesn't appear to be a debit card."                    |
  | Merve T         | 4012888888881881 | 000000000       | 1220            | 123 | "This card doesn't appear to be a debit card."                    |
  | Merve T         | 5555555555554444 | 000000000       | 1220            | 123 | "This card doesn't appear to be a debit card."                    |
  | Merve T         | 5105105105105100 | 000000000       | 1220            | 123 | "This card appears to be a prepaid debit card."                   |
  | Merve T         | 378282246310005  | 000000000       | 1220            | 123 | "This card doesn't appear to be a Visa or MasterCard debit card." |
  | Merve T         | 371449635398431  | 000000000       | 1220            | 123 | "This card doesn't appear to be a Visa or MasterCard debit card." |
  | Merve T         | 6011111111111117 | 000000000       | 1220            | 123 | "This card doesn't appear to be a Visa or MasterCard debit card." |
  | Merve T         | 6011000990139424 | 000000000       | 1220            | 123 | "This card doesn't appear to be a Visa or MasterCard debit card." |
  | Merve T         | 30569309025904   | 000000000       | 1220            | 123 | "This card doesn't appear to be a US debit card."                 |
  | Merve T         | 38520000023237   | 000000000       | 1220            | 123 | "This card doesn't appear to be a US debit card."                 |
  | Merve T         | 3530111333300000 | 000000000       | 1220            | 123 | "This card doesn't appear to be a US debit card."                 |
  | Merve T         | 3566002020360505 | 000000000       | 1220            | 123 | "This card doesn't appear to be a Visa or MasterCard debit card." |
  | Merve           | 4000056655665556 | 000000000       | 1220            | 123 | "Name must contain first name and last name."                     |
  | Merve T         | -4000000000000002| 000000000       | 1220            | 123 | "Your card was declined."                    |

  Scenario Outline: Expiration month and year validation
    Given the payment info form
    When I fill the form with
    | full_legal_name | card_number      | tax_id        | expiration_date  | cvc |
    | <full_legal_name>| <card_number>   | <tax_id>      | <expiration_date>|<cvc>|
    And I submit the form
    Then I should see the follow form error '<error>'

  Scenarios:
    | full_legal_name | card_number      | tax_id      | expiration_date  | cvc | error                                                                      |
    | Merve T         | 4000056655665556 | 000000000   | 1315             | 123 |  (instead, is Invalid date)                                                |
    | Merve T         | 4000056655665556 | 000000000   | 1270             | 123 | Your card's expiration year is invalid.                                    |

  Scenario Outline: CVC error check
    Given the payment info form
    When I fill the form with
    | full_legal_name | card_number      | tax_id      | expiration_date  | cvc
    | <full_legal_name>| <card_number>   | <tax_id>    | <expiration_date>|<cvc>|
    And I submit the form
    Then I should see the follow form error '<error>'

  Scenarios:
    | full_legal_name | card_number      | tax_id         | expiration_date |  cvc | error                                 |
    | Merve T         | 4000056655665556 | 000000000      | 1220            |  99  | security code is invalid.             |


  Scenario Outline: Payment Info Success
    Given the payment info form
    When I fill the form with
    | full_legal_name  | card_number      | tax_id      | expiration_date  | cvc
    | <full_legal_name>| <card_number>   | <tax_id>    | <expiration_date>|<cvc> |
    And I submit the form
    Then I should see success message that states '<success>'

  Scenarios:
  | full_legal_name | card_number       | tax_id         | expiration_date |  cvc  | success                                         |
  | Merve T         | 4000056655665556  | 000000000      | 1220            |  123  | "You have successfully added your payment info" |
  | Merve T         | 5200828282828210  | 000000000      | 1220            |  123  | "You have successfully added your payment info" |

