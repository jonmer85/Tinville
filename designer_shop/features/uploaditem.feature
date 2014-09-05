Feature: Upload Item Editor

As a designer, I would like the ability to upload an item to sell, including primary picture.
the content for this basic editor should include the following fields:
    - title
    - descriptions (rich text control)
    - product type (for example, shirts, pants etc)
    - sizes (only built in options)
    - quantity for each size

  @jon
  Scenario: Create Basic Item
	Given the demo shop editor
	When the add item tab is selected
	Then the add item form is displayed
	And I fill in the general add item fields with
    | Title     | Description                     | Category                 | Price | Image1          | SizeVariation |
    | Test item | <h1>Test Item Description</h1>  | Men > Clothing > Jackets | 10.00 | images/item.jpg | 1             |
	And I choose the size SM with row number 1 and I fill the following quantities and colors
    | Color | Quantity  |
    | Red   | 7         |
	And I submit this item
    Then I should see a confirmation message stating that the item was created
	Then I should see 1 product total
    
    
    
   @andy
   Scenario: Delete Basic Item
     Given the demo shop editor
     Given I have an item in the demo shop
     When I click the delete button for the product
     Then the product is removed
     And the shop editor refreshes in a minimized state  