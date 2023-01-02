Feature: Example usage
  As a BDD enthusiast,
  I want to learn all the features of pytest-bdd,
  So I can learn new things and get tasks done.

  # The "@" annotations are tags
  # One feature can have multiple scenarios
  # The lines immediately after the feature title are just comments

  @example
  Scenario: I test passing state between steps
    Given I put "Bill" into the world
    Then the world contains "Bill"


