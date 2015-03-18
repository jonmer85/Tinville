Feature: Designer Shop Color Selection

  In order to select a color for the designer shop
  As a designer
  I want to have a menu that allows me to choose a color for the shop

  Scenario: Color Menu
	Given the demo shop editor
	When the color picker button is pressed
	Then the color picker wheel is displayed
	And the color picker textbox is displayed
	And the create button is displayed
    And a color is submitted "#fb1c0e"
    Then The selected color is applied to the components of the shop "rgb(251, 28, 14)"
    And the text color of shop menu is applied "rgb(231, 229, 230)"
    And the color picker button is pressed
	Then the color picker wheel is displayed
	And the color picker textbox is displayed
	And the create button is displayed
    And a color is submitted "#f7f3f3"
    Then The selected color is applied to the components of the shop "rgb(247, 243, 243)"
    And the text color of shop menu is applied "rgb(119, 119, 119)"

  Scenario: AGW 214 - Colorpicker
    Given the demo shop editor
	When the color picker button is pressed
	Then the color picker wheel is displayed
	And the color picker textbox is displayed
	And the create button is displayed
    And the tinville orange color f46430 is submitted
    Then an exception Tinville Branding is not Allowed to be Used is thrown