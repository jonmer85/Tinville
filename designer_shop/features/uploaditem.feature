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
    | Title     | Description                     | Category                 | Price | Image1             | Image2             | SizeVariation |
    | TestItem1 | <h1>Test Item Description</h1>  | Men > Clothing > Jackets | 10.00 | images/item1_1.jpg | images/item1_2.jpg | 1
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
    And my primary image item1_1 and secondary image item1_2 are visible

  Scenario: Create Basic Item on Demo Shop using size dimensions
	Given the demo shop editor
	Then I should see 3 product total
    When the add item tab is selected
	And I fill in the general add item fields with
    | Title     | Description                     | Category                 | Price | Image1             | Image2              | SizeVariation |
    | TestItem1 | <h1>Test Item Description</h1>  | Men > Clothing > Jackets | 10.00 | images/item2_1.jpg | images/item2_2.jpg  |  2            |
	And I choose the sizeX 32 and the sizeY 34 with row number 1 and I fill the following quantities and colors
    | Color | Quantity  |
    | Red   | 10        |
    | Blue  | 3         |
	And I choose the sizeX 28.5 and the sizeY 34.7 with row number 2 and I fill the following quantities and colors
    | Color | Quantity  |
    | Green | 5         |
    | Blue  | 1         |
    And I submit this item
    Then I should see a confirmation message stating that the item was created
	Then I should see 4 product total
    When I click on the "TestItem1" item
    Then my color, quantity, and size selections are
    | Color  | Size           | Quantity |
    | Red    | 32.0 x 34.0    | 10       |
    | Blue   | 32.0 x 34.0    | 3        |
    | Blue   | 28.5 x 34.7    | 1        |
    | Green  | 28.5 x 34.7    | 5        |
    And my primary image item2_1 and secondary image item2_2 are visible

  Scenario: Create Basic Item on Demo Shop using size number
	Given the demo shop editor
	Then I should see 3 product total
    When the add item tab is selected
	And I fill in the general add item fields with
    | Title     | Description                     | Category                 | Price | Image1             | Image2              | SizeVariation |
    | TestItem1 | <h1>Test Item Description</h1>  | Men > Clothing > Jackets | 10.00 | images/item3_1.jpg | images/item3_2.jpg  | 3             |
	And I choose the sizenumber 5 with row number 1 and I fill the following quantities and colors
    | Color | Quantity  |
    | Red   | 10        |
    | Blue  | 3         |
	And I choose the sizenumber 8.5 with row number 2 and I fill the following quantities and colors
    | Color | Quantity  |
    | Green | 5         |
    | Blue  | 1         |
    And I submit this item
    Then I should see a confirmation message stating that the item was created
	Then I should see 4 product total
    When I click on the "TestItem1" item
    Then my color, quantity, and size selections are
    | Color  | Size | Quantity |
    | Red    | 5.0  | 10       |
    | Blue   | 5.0  | 3        |
    | Blue   | 8.5  | 1        |
    | Green  | 8.5  | 5        |
    And my primary image item3_1 and secondary image item3_2 are visible


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
    | Red    | XS    | 10       |
    | Blue   | XS    | 10       |
    | Red    | SM    | 4        |
    | Blue   | SM    | 10       |
    | White  | SM    | 1        |
    | Black  | XL    | 8        |
    And my primary image is different from the original


  Scenario: Delete a color/quantity row on basic item from Demo Shop
	Given the demo shop editor
	Then I should see 3 product total
    When I click the edit button on the basic size set product
    And the edit item tab is selected
    And I expand the sizes group
    And I add a new color to the size set product
    And I delete an existing color
    And I submit this item
    Then I should see a confirmation message stating that the item was updated
	Then I should see 3 product total
    When I click on the "TestSizeSetItem" item
    Then my color, quantity, and size selections are
    | Color  | Size  | Quantity |
    | Red    | XXS   | 10       |
    | Blue   | XXS   | 10       |
    | Red    | XS    | 10       |
    | Blue   | XS    | 10       |
    | Blue   | SM    | 10       |
    | White  | SM    | 1        |


  Scenario: Delete a size row on basic item from Demo Shop
	Given the demo shop editor
	Then I should see 3 product total
    When I click the edit button on the basic size set product
    And the edit item tab is selected
    And I expand the sizes group
    And I add a new size to the size set product
    And I delete an existing size
    And I submit this item
    Then I should see a confirmation message stating that the item was updated
	Then I should see 3 product total
    When I click on the "TestSizeSetItem" item
    Then my color, quantity, and size selections are
    | Color  | Size  | Quantity |
    | Red    | XXS   | 10       |
    | Blue   | XXS   | 10       |
    | Red    | XS    | 10       |
    | Blue   | XS    | 10       |
    | Black  | XL    | 8        |


  Scenario: Delete Basic Item
     Given the demo shop editor
     Given I have an item in the demo shop
     When I click the delete button for the product
     And I click ok on the confirmation
     Then the product is removed
     And the shop editor refreshes in a minimized state
