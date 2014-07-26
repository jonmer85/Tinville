Feature: Item Detail
    In order to browse clothing
    As a customer
    I want to view a designer's shop and select an item
    and view it's detail. I should be able to select color, size and quantity

    Scenario: Navigate to Item Detail page
        Given I am on the Demo Shop
        Given I have a the following item in a shop
            | attribute | value |
            | Name      | "My Test Item" |
            | Description | "This is my item description" |
            | Price | "12.99" |
            | Image1 | /media/image1 |
            | Image2 | /media/image2 |
            | Image3 | /media/image3 |
            | Image4 | /media/image4 |
            | Image5 | /media/image5 |
            | SizeType | SizeSet |
            | Size1 | SM |
            | Color1 | Blue |
            | Quantity1 | 5 |
            | Color2 | Red |
            | Quantity2 | 7 |
            | Size2 | MD |
            | Color1 | Yellow |
            | Quantity1 | 15 |
            | Color2 | Red |
            | Quantity2 | 12 |
        When I click on an item
        Then the item detail page is displayed

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

    Scenario: Default Values
        Given: I am on an item details page
        Then the default values for an item are as follows
            | itemColorSelection | "Choose a Color" |
            | itemSizeSelection | "Choose a Size" |
            | buyQuantity | 1 |

    Scenario: Select Color
        Given I am on an item detail page
        When I select the color Blue
        Then my itemColorSelection is Blue

    Scenario: Select Size
        Given I am on an item detail page

    Scenario: Select Quantity
        Given I am on an item detail page

