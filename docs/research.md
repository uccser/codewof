# Research

This document contains notes regarding deploying the website in research mode.

The research application has been written to prevent users from accessing pages of website without meeting a series of conditions:

- Admins can always access all pages of the website.
- Some pages are always able to be accessed (homepage, registration page, contact page, etc).
- Users must be logged in.
- Users must agree to consent form.
- Users must view between start and end dates of research (can skip this step by additional permission on users).

The aim of the application is for research studies to be hosted at a special domain, parallel to the existing production and staging websites.
The database should be cleared before and after the study. A basic API allows the researcher to access the database with programs.

## Configuring research settings

Configuring the research application can be done using the following three files:

- `codewof/research/settings.py`
- `codewof/research/forms.py`
- `codewof/templates/research/study_description.html`

The research mode can only be turned on in the staging deployment and local development.

## Deploying research website

The `docker-compose.prod.yml` needs to be modified in the following places:

- The image for `django` needs to be set.
- The two calls to the `${CODEWOF_DOMAIN}` need to replaced with the literal value.
- The traefik router `codewof-django` needs to be renamed so it doesn't conflict.
- All secrets and configuration values should be duplicated and altered.

Deploy the stack with `docker stack deploy STACK_NAME -c docker-compose.prod.yml`.

Once the website is deployed, you will want to run `updatedata` and `createsuperuser`.
You will also want to set the correct site domain under 'Sites' in the admin interface.
