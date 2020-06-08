# Changelog

## 2.0.0

Adds gamification elements (points and achievements) to the website, including for all previous submissions for each user.

- Add gamification system that allows users to earn points and achievements.
- Add ability for the CodeWOF server to recalculate a user's points and achievements from their past attempts.
- Improve the CodeWOF admin site with more information and filtering options.
- Update Django from 2.1.5 to 2.2.3.
- Dependency updates:
    - Remove django-coverage-plugin.
    - Update coverage from 4.5.4 to 5.1.
    - Update django-activeurl from 0.1.12 to 0.2.0.
    - Update django-allauth from 0.39.1 to 0.41.0.
    - Update django-ckeditor from 5.7.1 to 5.9.0.
    - Update django-crispy-forms from 1.7.2 to 1.9.0.
    - Update django-debug-toolbar from 2.0 to 2.2.
    - Update django-extensions from 2.2.1 to 2.2.9.
    - Update django-modeltranslation from 0.13.3 to 0.14.4.
    - Update django-model-utils from 3.2.0 to 4.0.0.
    - Update django-recaptcha from 2.0.5 to 2.0.6.
    - Update django-redis from 4.10.0 to 4.11.0.
    - Update django-storages from 1.7.1 to 1.9.1.
    - Update google-api-python-client from 1.7.11 to 1.7.12.
    - Update google-auth from 1.6.3 to 1.12.0.
    - Update google-cloud-logging from 1.12.1 to 1.15.0.
    - Update mypy from 0.720 to 0.770.
    - Update Pillow from 6.1.0 to 7.0.0.
    - Update pydocstyle from 4.0.1 to 5.0.2.
    - Update pytest from 5.1.1 to 5.4.1.
    - Update pytest-django from 3.5.1 to 3.8.0.
    - Update PyYAML from 5.1.2 to 5.3.1.
    - Update Sphinx from 2.2.0 to 3.0.4.

## 1.5.3

- Use default settings for split health checks.

## 1.5.2

- Split GCP health check URLs.

## 1.5.1

- Update GCP health checks.

## 1.5.0

- Add 7 new questions.
- Fix test case where no argument was passed for the total of evens question. Fixes #101
- Fix error in example of the driver speed question.
- Do not allow use of tab characters to indent code. Fixes #103
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
- Dependency updates:
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
