# Changelog

## 1.2.1

- Don't save question attempt if same as previous attempt. Fixes #37.
- Emphasise whether functions should return or print. Fixes #47.
- Replace sign up button on homepage to link to dashboard if user is logged in.
- Remove default ACL for media files as permissions set with bucket policy.

## 1.2.0

- Add 'How to use' section and dropzone highlighting for Parson's Problems. Fixes #35.
- Pick different daily questions for each user. Fixes #43.
- Add title attributes for each webpage.
- Prevent users from removing user type. Fixes #41.
- Add logging for choosing user daily questions.

## 1.1.1

- Fix bug where home link in navbar didn't highlight.
- Set automated production deployment to master branch.

## 1.1.0

- Add user dashboard listing daily questions.
- Add 9 new questions.
- Redesign homepage.
- Add privacy policy, terms of service, and cookie policy.
- Fix reCAPTCHA checkers.
- Fix bug where users could register for a research study with no groups.
- Provide link to dashboard after questions.
- Simplify available navbar items.

## 1.0.0

Initial release of codeWOF website, containing the following key features:

- Allows users to create an account with email verification.
- List Python questions in various question types including:
    - Program questions
    - Function questions
    - Parson's problems
    - Debugging questions
- Questions are run browser side in JavaScript for simplicity and security.
- Questions are open source and easily extended.
- List research studies, and allow user to register for these.
- Project based off Django system used by UCCSER for consistency.

## 0.1.0

Initial prototype developed in 2018.
