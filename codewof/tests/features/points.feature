Feature: Points

#Test initial points are zero
Scenario: User profile is created
  Given a user with ID 1 is logged in
  When their account is created
  Then their profile's points are equal to 0

#Test bonus point for first correct login
Scenario: User solves a question on first attempt
  Given a user with ID 1 is logged in
  And their profile points are 0
  And they have not attempted the "Print CodeWOF" question
  When they solve the "Print CodeWOF" question
  Then the user's points equal 11

#Test for question that has previously been attempted
Scenario: User solves an attempted question
  Given a user with ID 1 is logged in
  And their profile points are 0
  And they have attempted the "Print CodeWOF" question
  When they solve the "Print CodeWOF" question
  Then the user's points equal 10

#Test for question that has been attempted but not solved
Scenario: User attempts a question
  Given a user with ID 1 is logged in
  And their profile points are 0
  When they attempt the "Print CodeWOF" question without solving it
  Then the user's points equal 0

#Test for question that has previously been solved
Scenario: User attempts a question
  Given a user with ID 1 is logged in
  And their profile points are 10
  And they have already solved the "Print CodeWOF" question
  When they solve the "Print CodeWOF" question
  Then the user's points equal 10

#Test for points earned with first attempt badge
Scenario: User earns badge for one attempt
  Given a user with ID 1 is logged in
  And their profile points are 0
  And they have not earned the badge for attempting one question
  When they attempt the "Print CodeWOF" question
  Then the user's points equal 10

  #Test for points earned with five attempts badge
  Scenario: User earns badge for five attempts
    Given a user with ID 1 is logged in
    And their profile points are 10
    And they have not earned the badge for attempting five questions
    And they have made 4 attempts in total
    When they attempt the "Print CodeWOF" question
    Then the user's points equal 30
