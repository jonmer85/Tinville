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
	And I fill in the general add item fields