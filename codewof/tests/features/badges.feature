Feature: Badges

Scenario: User profile is created
  Given a user with ID 1 exists
  When their account is created
  Then their profile has 0 badges
