Feature: Designer Shop Color Selection

  In order to select a color for the designer shop
  As a designer
  I want to have a menu that allows me to choose a color for the shop

  Scenario: Color Menu
	Given the demo shop editor
	When the color tab is selected
	Then the color picker wheel is displayed
	And the color picker textbox is displayed
	And the create button is displayed
    And a color is submitted
    The selected color is applied to the components of the shop

  Scenario: AGW 214 - Colorpicker
    Given the demo shop editor
	When the color tab is selected
	Then the color picker wheel is displayed
	And the color picker textbox is displayed
	And the create button is displayed
    And the tinville orange color f46430 is submitted
    The an exception Tinville Branding is not Allowed to be Used is thrown