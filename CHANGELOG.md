# Changelog

## 5.1.1

- Submission table now resets as soon as you click "run code" to make timeouts more obvious
- Reworked worker creation/termination to fix bug where valid attempts after a timeout would still fail
- Error messages now changed to "Bad input on line <line number>" instead of stacktrace (reproducing previous functionality)

## 5.1.0

- Replaced Skulpt with Pyodide
    - Website now uses Python 3.12
- Added the /information endpoint for user study information sheet
- Fixed parsons problems
    - Dragging code blocks now works
- Added a COSC121 user type

## 5.0.2

- Add Plausible analytics.
- Dependency updates:
    - Update autoprefixer from 10.4.12 to 10.4.13.
    - Update cssnano from 5.1.13 to 5.1.14.
    - Update django from 3.2.15 to 3.2.16.
    - Update psycopg2 from 2.9.4 to 2.9.5.
    - Update pytz from 2022.4 to 2022.5.
    - Update pytest from 7.1.3 to 7.2.0.

## 5.0.1

- Fix bug where a sequence of code characters could stop the JavaScript file from parsing correctly.
- Delete management command with duplicated command name
- Dependency updates:
    - Update dependabot/fetch-metadata from v1.3.3 to v1.3.4.
    - Update docker/login-action from v2.0.0 to v2.1.0.
    - Update docker/build-push-action from v3.1.1 to v3.2.0.
    - Update postcss from 8.4.16 to 8.4.18.
    - Update yargs from 17.5.1 to 17.6.0.
    - Update psycopg2 from 2.9.3 to 2.9.4.
    - Update pytz from 2022.2.1 to 2022.4.
    - Update django-modeltranslation from 0.18.4 to 0.18.5.
    - Update mypy from 0.971 to 0.982.
    - Update coverage from 6.4.4 to 6.5.0.
    - Update django-debug-toolbar from 3.6.0 to 3.7.0.

## 5.0.0

- Add question recommendations to users.
    - Track proficiency of users' programming skills, using this information to suggest exercises for the user to perform.
- Add descriptive tags for each programming question.
- Add filtering of questions by question type, difficulty, contexts, and concepts.
- Add 15 new Python 3 questions.
- Contact emails show which domain they were sent from.
- Add URL for website status information.
- Allow 'likes' to be viewed in the admin interface.
- Disable API on production website.
- Use HTML templates for emails, replacing current plaintext emails.
- Add `update_data` management command for consistency across UCCSER repositories.
- Enable CORS headers for providing version information across domains.
- Set Gulp to watch for changed files and rebuild them as required.
- Update project to use uccser-development-stack v3.
- Auto-merge minor dependency updates (this includes minor and patch updates).
- Allow all dependency update pull requests to be created (remove open limit on Dependabot).
- Add OCI labels to Django Docker image.
- Ignore updates to non-LTS Django packages.
- Remove outdated helper script.
- Remove unused Travis CI configuration file.
- Remove unused Browser Sync functionality within Gulpfile.
- Dependency updates:
    - Add django-cors-headers 3.13.0.
    - Update ansi-colors from 4.1.1 to 4.1.3.
    - Update argon2-cffi from 19.2.0 to 21.3.0.
    - Update autoprefixer from 10.3.1 to 10.4.12.
    - Update bootstrap from 4.6.0 to 4.6.2.
    - Update clipboard from 2.0.8 to 2.0.11.
    - Update codemirror from 5.63.1 to 5.65.1.
    - Update coverage from 6.0.2 to 6.4.4.
    - Update cssnano from 5.0.8 to 5.1.13.
    - Update django from 3.2.6 to 3.2.15.
    - Update django-allauth from 0.45.0 to 0.51.0.
    - Update django-anymail[mailgun] from 7.0.0 to 8.6.
    - Update django-ckeditor from 6.1.0 to 6.5.1.
    - Update django-crispy-forms from 1.9.0 to 1.14.0.
    - Update django-debug-toolbar from 3.2.2 to 3.6.0.
    - Update django-environ from 0.4.5 to 0.9.0.
    - Update django-extensions from 3.0.8 to 3.2.1.
    - Update django-filter from 21.1 to 22.1.
    - Update django-model-utils from 4.1.1 to 4.2.0.
    - Update django-modeltranslation from 0.17.3 to 0.18.4.
    - Update django-recaptcha from 2.0.6 to 3.0.0.
    - Update djangorestframework from 3.12.4 to 3.14.0.
    - Update factory-boy from 2.12.0 to 3.2.1.
    - Update fancy-log from 1.3.3 to 2.0.0.
    - Update flake8-docstrings from 1.5.0 to 1.6.0.
    - Update flake8-quotes from 2.1.1 to 3.3.1.
    - Update fuse.js from 6.4.6 to 6.6.2.
    - Update gulp-postcss from 9.0.0 to 9.0.1.
    - Update gulp-sass from 5.0.0 to 5.1.0.
    - Update intro.js from 4.2.2 to 6.0.0.
    - Update jquery from 3.6.0 to 3.6.1.
    - Update mypy from 0.782 to 0.971.
    - Update postcss from 8.3.6 to 8.4.16.
    - Update psycopg2 from 2.9.1 to 2.9.3.
    - Update pytest from 6.2.5 to 7.1.3.
    - Update pytest-django 3.9.0 to 4.5.2.
    - Update pytest-sugar from 0.9.4 to 0.9.5.
    - Update pytz from 2019.3 to 2022.2.1.
    - Update sass from 1.42.1 to 1.55.0.
    - Update sortablejs from 1.8.4 to 1.15.0.
    - Update whitenoise from 5.3.0 to 6.2.0.
    - Update yargs from 7.1.1 to 7.5.1.
    - Remove browser-sync 2.27.5.

## 4.0.0

- Add user groups, including invite functionality.
- Add reminder emails, along with the ability for users to customise the reminder frequency.
- Add 34 new Python 3 questions.
- Move website from Google Cloud Platform to Docker Swarm hosted at the University of Canterbury.
    - Modifies website infrastructure to use Docker Swarm, running all website components as services.
    - Static files are now served by Django.
    - Use GitHub actions for automated workflows.
    - Simplify static file pipeline, runs as separate Docker service.
- Rewrite research application, allowing the entire website to function in mode requiring registration and consent acceptance for research purposes. #374
- Add management command for easily creating an admin account.
- Update reCAPTCHA v2 checkbox to v3.
- Switch to GitHub dependency manager.
- Dependency updates:
    - Add ansi-colors 4.1.1.
    - Add browser-sync 2.27.5.
    - Add child_process 1.0.2.
    - Add cssnano 5.0.8.
    - Add django-test-without-migrations 0.6.
    - Add fancy-log 1.3.3.
    - Add gulp-concat 2.6.1.
    - Add gulp-imagemin 5.0.3.
    - Add pixrem 5.0.0.
    - Add postcss 8.3.6.
    - Add sass 1.42.1.
    - Add whitenoise 5.3.0.
    - Update autoprefixer from 9.5.1 to 10.3.1.
    - Update bootstrap from 4.3.1 to 4.6.0.
    - Update browserify from 16.2.3 to 17.0.0.
    - Update clipboard from 2.0.6 to 2.0.8.
    - Update codemirror from 5.47.0 to 5.63.1.
    - Update coverage from 5.2.1 to 6.0.2.
    - Update details-element-polyfill from 2.3.1 to 2.4.0.
    - Update django from 2.2.3 to 3.2.6.
    - Update django-allauth from 0.41.0 to 0.45.0.
    - Update django-autoslug-iplweb 1.9.5 to django-autoslug 1.9.8 (name change).
    - Update django-ckeditor from 5.9.0 to 6.1.0.
    - Update django-debug-toolbar from 2.2 to 3.2.2.
    - Update django-filter from 2.2.0 to 21.1.
    - Update django-model-utils from 4.0.0 to 4.1.1.
    - Update django-modeltranslation from 0.14.4 to 0.17.3.
    - Update djangorestframework from custom UCCSER variant to official 3.12.4.
    - Update flake8 from sha:20906d43 to 4.0.1.
    - Update fuse.js from 3.4.4 to 6.4.6.
    - Update gulp-filter from 5.1.0 to 7.0.0.
    - Update gulp-if from 2.0.2 to 3.0.0.
    - Update gulp-postcss from 8.0.0 to 9.0.0.
    - Update gulp-sass from 4.0.2 to 5.0.0.
    - Update gulp-sourcemaps 2.6.5 to 3.0.0.
    - Update gulp-tap from 1.0.1 to 2.0.0.
    - Update gulp-terser from 1.1.7 to 2.1.0.
    - Update gunicorn from 20.0.4 to 20.1.0.
    - Update intro.js from 2.9.3 from 4.2.2.
    - Update jquery from 3.4.1 to 3.6.0.
    - Update pep8-naming from 0.9.1 to 0.12.1.
    - Update popper.js from 1.15.0 to 1.16.1.
    - Update postcss-flexbugs-fixes from 4.1.0 to 5.0.2.
    - Update psycopg2 from 2.8.6 to 2.9.1.
    - Update pydocstyle from 5.1.1 to 6.1.1.
    - Update pytest from 6.0.1 to 6.2.5.
    - Update python-dateutil from 2.8.1 to 2.8.2.
    - Update PyYAML from 5.3.1 to 5.4.1.
    - Update verto from 0.10.0 to 1.0.1.
    - Update yargs from 13.2.4 to 17.1.1.
    - Remove @babel/core.
    - Remove @babel/preset-env.
    - Remove del.
    - Remove django-redis.
    - Remove django-storages[google].
    - Remove filetype.
    - Remove google-api-python-client.
    - Remove google-auth.
    - Remove google-cloud-logging.
    - Remove gulp-babel.
    - Remove gulp-jshint.
    - Remove gulp-notify.
    - Remove gulp-rename.
    - Remove gulp-util.
    - Remove gulplog.
    - Remove jshint-stylish.
    - Remove jshint.
    - Remove node-gyp.
    - Remove Pillow.
    - Remove psycopg2-binary.
    - Remove python-slugify.
    - Remove redis.
    - Remove request.
    - Remove run-sequence.
    - Remove Sphinx.

## 3.1.1

- Ensure footer is at the bottom of the page even when there is not enough content.
- Clarify error when the line number is greater than the number of lines in the users code.

## 3.1.0

- Add step by step introduction/tutorial to question pages.
- Add third party licence files.
- Update README.
- Dependency updates:
    - Update coverage from 5.1 to 5.2.1.
    - Update django-extensions from 2.2.9 to 3.0.8.
    - Update django-storages[google] from 1.9.1 to 1.10.
    - Update google-auth from 1.12.0 to 1.21.1.
    - Update google-cloud-logging from 1.15.0 to 1.15.1.
    - Update mypy from 0.770 to 0.782.
    - Update Pillow from 7.0.0 to 7.2.0.
    - Update psycopg2-binary from 3.0.4 to 3.2.1.
    - Update pydocstyle from 5.0.2 to 5.1.1.
    - Update pytest from 5.3.5 to 6.0.1.
    - Update pytest-django from 3.8.0 to 3.9.0.
    - Update pytest-sugar from 0.9.2 to 0.9.4.
    - Update Sphinx from 2.8.4 to 2.8.6.

## 3.0.0

Add style checker for beginners.

- Style checker for beginners is a freely accessible style checker.
    - Currently only Python 3 is supported.
    - Code is anonymously stored on the website for analysis and then instantly deleted.
    - Count of style issues triggered by submitted code are stored, but the code itself is not permanently stored.
    - Statistics of style issue occurence counts are publically visible.
- Dependency updates:
    - Add django-bootstrap-breadcrumbs 0.9.2.
    - Set flake8 to custom version that allows isolated configurations, to be updated to official release in next update.
    - Add flake8-docstrings 1.5.0.
    - Add flake8-quotes 2.1.1.
    - Add pep8-naming 0.9.1.

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
