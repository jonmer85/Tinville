Feature: Upload Item Editor

As a designer, I would like the ability to upload an item to sell, including primary picture.
the content for this basic editor should include the following fields:
    - title
    - descriptions (rich text control)
    - product type (for example, shirts, pants etc)
    - sizes (only built in options)
    - quantity for each size

  Scenario: Create Basic Item on Demo Shop using size sets
	Given the demo shop editor
	Then I should see 3 product total
    When the add item tab is selected
	And I fill in the general add item fields with
    | Title     | Description                     | Category                 | Price | Image1          | SizeVariation |
    | TestItem1 | <h1>Test Item Description</h1>  | Men > Clothing > Jackets | 10.00 | images/item.jpg | 1             |
	And I choose the size SM with row number 1 and I fill the following quantities and colors
    | Color | Quantity  |
    | Red   | 7         |
    | Blue  | 2         |
	And I choose the size LG with row number 2 and I fill the following quantities and colors
    | Color | Quantity  |
    | Green | 3         |
    | Blue  | 5         |
    And I submit this item
    Then I should see a confirmation message stating that the item was created
	Then I should see 4 product total
    When I click on the "TestItem1" item
    Then my color, quantity, and size selections are
    | Color  | Size  | Quantity |
    | Red    | SM    | 7        |
    | Blue   | SM    | 2        |
    | Blue   | LG    | 5        |
    | Green  | LG    | 3        |
    And my primary image is visible

  Scenario: Edit Basic Item on Demo Shop using size sets
	Given the demo shop editor
    And I plan to change the default image of the size set product
	Then I should see 3 product total
    When I click the edit button on the basic size set product
    And the edit item tab is selected
    And I fill in the general add item fields with
    | Title           | Description                         | Category                   | Price | Image1            | SizeVariation |
    | NewTestSizeSet  | <h1>New Test Item Description</h1>  | Women > Clothing > Pants   | 8.00  | images/walken.jpg | 1             |
    And I add a new color to the size set product
    And I change the quantity of one of the colors of the size set product
    And I add a new size to the size set product
    And I submit this item
    Then I should see a confirmation message stating that the item was updated
	Then I should see 3 product total
    When I click on the "TestSizeSetItem" item
    Then my color, quantity, and size selections are
    | Color  | Size  | Quantity |
    | Red    | XXS   | 10       |
    | Blue   | XXS   | 10       |
    | Red    | XS    | 4        |
    | Blue   | XS    | 10       |
    | Red    | SM    | 10       |
    | Blue   | SM    | 10       |
    | White  | SM    | 1        |
    | Black  | XL    | 8        |
    And my primary image is different from the original


  Scenario: Delete Basic Item
     Given the demo shop editor
     Given I have an item in the demo shop
     When I click the delete button for the product
     And I click ok on the confirmation
     Then the product is removed
     And the shop editor refreshes in a minimized state
