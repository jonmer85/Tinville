Feature: Item Detail
    In order to browse clothing
    As a customer
    I want to view a designer's shop and select an item
    and view it's detail. I should be able to select color, size and quantity

    @wip
    Scenario: Navigate to Item Detail page
        Given the demo shop
        Given I have an item in the demo shop
        When I click on the item
        Then the item detail page is displayed

    @wipitem
    Scenario: Visible the Item Detail page
        Given I am on an item detail page
        Then I can see the following elements
            | Class              |
            | shopItem           |
            | itemTitle          |
            | itemPrice          |
            | itemColorSelection |
            | itemSizeSelection  |
            | itemBuyQuantity    |
            | addToCart          |
            | itemDescription    |
            | sharingiscaring    |
            | itemselectedimage  |

    @wipitem
    Scenario: Default Values
        Given: I am on an item details page
        Then the default values for an item are as follows
            | itemColorSelection | "Choose a Color" |
            | itemSizeSelection | "Choose a Size" |
            | buyQuantity | 1 |

    @wipitem
    Scenario: Select Color
        Given I am on an item detail page
        When I select the color Blue
        Then my itemColorSelection is Blue

    @wipitem
    Scenario: Select Size
        Given I am on an item detail page
        When I try to select a size there are no options
        When I select a the Color Blue
        Then I should be
        Then

    @wipitem
    Scenario: Select Quantity
        Given I am on an item detail page

