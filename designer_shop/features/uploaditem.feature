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


    sizeVariationElement = world.browser.find_element_by_name('sizeVariation')
    scroll_to_element(sizeVariationElement)
    variationSelection = Select(sizeVariationElement)
    time.sleep(2)
    variationSelection.select_by_value("1")  # Size Set
    sizeSetSelectionElement = world.browser.find_element_by_name('sizeSetSelectionTemplate0_sizeSetSelection')
    scroll_to_element(sizeSetSelectionElement)
    sizeSetSelection = Select(sizeSetSelectionElement)
    sizeSetSelection.select_by_visible_text(sizeset)
    time.sleep(1)
    colorSelection = Select(world.browser.find_element_by_name('sizeSetSelectionTemplate0_colorSelection0'))
    colorSelection.select_by_visible_text(color)
    world.browser.find_element_by_name('sizeSetSelectionTemplate0_quantityField0').send_keys(quantity)