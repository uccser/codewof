# Changelog

## 1.5.0
- Add 7 new questions.
- Fix test case in total of evens question. Fixes #101
- Fix error in example of driver speed question.
- Add endpoints to API.

## 1.4.0

- Add 37 new questions.
- Add API.

## 1.3.1

- Remove ride share question.
- Enable modification of questions via admin interface.

## 1.3.0

- Add 16 new questions.
- Add summary page for question creators.
- Improve access to information for research studies:
    - Provide links to study researchers for easy contacting.
    - Add summary page for researchers.
    - Allow download of research study attempts for researchers.
- Fix bug where whitespace of user code in attempt wasn't shown in admin interface.
- Fix bug where sender's email address is not listed on contact us forms sent to admin.
- General typo fixes and question clarifications.
- Dependencies changes:
    - Update django-recaptcha from 2.0.4 to 2.0.5.
    - Update google-api-python-client from 1.7.10 to 1.7.11.
    - Update pydocstyle from 4.0.0 to 4.0.1.
    - Update pytest from 5.0.1 to 5.1.1.
    - Update Sphinx from 2.1.2 to 2.2.0.

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
