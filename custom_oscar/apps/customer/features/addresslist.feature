Feature: Custom Address List Page

  As a customer
  I would like the ability to add, delete, update, and mark existing addresses as shipping, billing,
  and shop shipping addresses
  So that I can have the system automatically reference these addresses when an address is required

  Initially, I am only testing the new shop shipping address that Oscar was extended to support



  Scenario: Add an Address with no default address types
    Given I access the addresses page as a new designer
    When I add a new address
    Then I should not see any default address types
    And I should see all available designer address types as options to be added to the address

  Scenario: Add an Address and mark as shipping address
    Given I access the addresses page as a new designer
    When I add a new address
    And I mark the address as the shipping address
    Then the shipping address badge is shown

  Scenario: Add an Address and mark as shop address
    Given I access the addresses page as a new designer
    When I add a new address
    And I mark the address as the shop address
    Then the shop address badge is shown

  @jon
  Scenario: Add an Address As a Shopper and ensure they cannot mark it as a Shop Shipping Address
    Given I access the addresses page as a new shopper
    When I add a new address
    Then I should not see any default address types
    And I should see all available shopper address types as options to be added to the address

#  Scenario: Add an Address and mark as billing address
#
#  Scenario: Add an Address, mark as shipping address, create a new address,
#            change shipping address to new address
#
#  Scenario: Add an Address, mark as shop shipping address, create a new address,
#            change shop shipping address to new address