Feature: Points

Scenario: User profile is created
  Given a user with ID 1 exists
  When their account is created
  Then their profile's points are equal to 0

Scenario: User answers
