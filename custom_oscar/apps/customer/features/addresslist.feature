Feature: Custom Address List Page

  As a customer
  I would like the ability to add, delete, update, and mark existing addresses as shipping, billing,
  and shop shipping addresses
  So that I can have the system automatically reference these addresses when an address is required

  Initially, I am only testing the new shop shipping address that Oscar was extended to support


  Scenario: Add an Address for designer and it should automatically be marked as the shop shipping address
    Given I access the addresses page as a new designer
    When I add a new address
    Then the shop address badge is shown
    And I should see all but shop shipping address available designer address types as options to be added to the address

  Scenario: Add an Address and mark as shipping address
    Given I access the addresses page as a new designer
    When I add a new address
    And I mark the address as the shipping address
    Then the shipping address badge is shown

  @testandy
  Scenario: Add an Address As a Shopper and ensure they cannot mark it as a Shop Shipping Address
    Given I access the addresses page as a new shopper
    When I add a new address
    Then I should not see any default address types
    And I should see all available shopper address types as options to be added to the address

  @tommy
  Scenario: Add an Address that is prepended with white space
    Given I access the addresses page as a new shopper
    When I Add a new address that is prepended with white space
    Then I should not see any default address types

  @tommy
  Scenario: Add an Address that is appended with white space
    Given I access the addresses page as a new shopper
    When I Add a new address that is appended with white space
    Then I should not see any default address types


#  Scenario: Add an Address and mark as billing address
#
#  Scenario: Add an Address, mark as shipping address, create a new address,
#            change shipping address to new address
#
#  Scenario: Add an Address, mark as shop shipping address, create a new address,
#            change shop shipping address to new address