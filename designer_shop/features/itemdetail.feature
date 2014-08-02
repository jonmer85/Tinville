Feature: Item Detail
    In order to browse clothing
    As a customer
    I want to view a designer's shop and select an item
    and view it's detail. I should be able to select color, size and quantity

    Scenario: Navigate to Item Detail page
        Given the demo shop
        Given I have an item in the demo shop
        When I click on the item
        Then the item detail page is displayed
    @wip
    Scenario: Visible the Item Detail page
        Given I am on an item detail page
        Then I can see the following elements
            | Class              |
            | shopItemDetail     |
            | itemTitle          |
            | itemPrice          |
            | itemColorSelection |
            | itemSizeSelection  |
            | itemBuyQuantity    |
            | addToCart          |
            | itemDescription    |
            | sharingiscaring    |
            | selectedImage      |

    Scenario: Default Values
        Given I am on an item detail page
        Then the default values for an item are as follows
            | Class              | DefaultValue     |
            | itemColorSelection | "Choose a Color" |
            | itemSizeSelection  | "Choose a Size"  |
            | buyQuantity        | 1                |

    Scenario: Select Color
        Given I am on an item detail page
        When I select the color Blue
        Then my color is Blue

    Scenario: Select Size
        Given I am on an item detail page
        When I try to select a size there are no options
        When I select the color Blue
        When I select the size Sm
        Then my size is Sm

    Scenario: Item Buy Quantity
        Given I am on an item detail page
        When I select the color Blue
        When I select the size Sm
        When I select a quantity of 5
        Then my quantity is 5

    Scenario: Item Stock Quantity
        Given I am on an item detail page
        When I select the color Blue
        When I select the size Sm
        Then my stock quantity is 10
