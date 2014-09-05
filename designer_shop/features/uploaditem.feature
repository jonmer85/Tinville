Feature: Upload Item Editor

As a designer, I would like the ability to upload an item to sell, including primary picture.
the content for this basic editor should include the following fields:
    - title
    - descriptions (rich text control)
    - product type (for example, shirts, pants etc)
    - sizes (only built in options)
    - quantity for each size

  Scenario: Create Basic Item
	Given the demo shop editor
	When the add item tab is selected
	Then the add item form is displayed
	And I fill in the general add item fields with
    | Title       | Description                       | Price   | Image1            |
    | 'Test item' | '<h1>Test Item Description</h1>'  | '10.00' | 'images/item.jpg' |
	And I fill the following variants
    | SizeVariation | SizeSet | SizeX | SizeY | SizeNum | Quantity  |
    | Set           | SM      |       |       |         | 7         |
	And I submit this item
	Then I should see 1 product total
    
    
    
   @andy
   Scenario: Delete Basic Item
     Given the demo shop editor
     Given I have an item in the demo shop
     When I click the delete button for the product
     Then the product is removed
     And the shop editor refreshes in a minimized state  