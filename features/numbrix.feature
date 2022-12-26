Feature: Online Numbrix Solver
  As a lazy puzzler doer,
  I want to use a service to solve puzzles for me,
  So I can more on to other puzzles.

  # The "@" annotations are tags
  # One feature can have multiple scenarios
  # The lines immediately after the feature title are just comments

  @numbrix
  Scenario: Basic Numbrix Solving
    Given the puzzle server is running
    Given the following Numbrix puzzle
        """
            #     |  A  |  B  |  C  |  D  |  E  |  F  |
            # ----‖=====‖=====‖=====‖=====‖=====‖=====‖
            #   1 |  4  |     |     |     |     |  29 |
            #   2 |     |  2  |  33 |  26 |  27 |     |
            #   3 |     |     |     |     |  24 |     |
            #   4 |     |  36 |     |     |  21 |     |
            #   5 |     |  11 |  12 |  19 |  18 |     |
            #   6 |  9  |     |     |     |     |  16 |
            # ----‖=====‖=====‖=====‖=====‖=====‖=====‖
        """

    When I submit this puzzle to the solver
    Then I get the following result back
        """
            #     |  A  |  B  |  C  |  D  |  E  |  F  |
            # ----‖=====‖=====‖=====‖=====‖=====‖=====‖
            #   1 |  4  |     |     |     |     |  29 |
            #   2 |     |  2  |  33 |  26 |  27 |     |
            #   3 |     |     |     |     |  24 |     |
            #   4 |     |  36 |     |     |  21 |     |
            #   5 |     |  11 |  12 |  19 |  18 |     |
            #   6 |  9  |     |     |     |     |  16 |
            # ----‖=====‖=====‖=====‖=====‖=====‖=====‖
        """
