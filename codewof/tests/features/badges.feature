Feature: Badges

#check badge on creation
Scenario: User profile is created
  Given a user with ID 1 exists
  When their account is created
  Then their profile has 1 badge

Scenario: User profile earns badge for one attempt
  Given a user with ID 1 exists
  And they have not earned the badge for one attempt
  When the user attempts the "Print CodeWOF" question without solving it
  Then the user earns a badge for one attempt made

Scenario: User profile earns badge for one question solved
  Given a user with ID 1 exists
  And they have not earned the badge for solving one question
  When the user solves the "Print CodeWOF" question
  Then the user earns a badge for one question solved

Scenario: User profile earns two badges on first question
  Given a user with ID 1 exists
  And they have not earned the badge for solving one question
  And they have not attempted the "Print CodeWOF" question
  And they have not earned the badge for one attempt
  When the user solves the "Print CodeWOF" question
  Then the user earns the one question solved badge and the one attempt made badge
