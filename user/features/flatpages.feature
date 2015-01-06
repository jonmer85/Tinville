Feature: Flatpages

@senay
  Scenario: Goto About page
	When I click the flatpage of "/about/"
	Then I check if that page is active of id "About"
