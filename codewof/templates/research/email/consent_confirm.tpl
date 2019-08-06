{% extends "mail_templated/base.tpl" %}

{% block subject %}
    You have successfully registered for "{{ study.title }}" study
{% endblock %}

{% block body %}
Dear {{ user.first_name }},

Thank you for registering for the "{{ study.title }}" study.
Below is a copy of the information sheet, and your signed consent form.

{{ study.description|striptags }}

-------------------------------------------------------
Signed Consent Form
-------------------------------------------------------

{% for field in form %}{% if field.value %}I AGREE{% else %}I DO NOT AGREE{% endif %} - {{ field.label }}{% endfor %}
- Email address: {{ user.email }}
- Date: {{ registration.datetime|time:"g:i A" }} {{ registration.datetime|date:"l j F Y" }}

Thank you,

The codeWOF team
{% endblock %}

{% block html %}
    <p>Dear {{ user.first_name }},</p>

    <p>
        Thank you for registering for the "{{ study.title }}" study.
        Below is a copy of the information sheet, and your signed consent form.
    </p>

    {{ study.description|safe }}

    <h2>Consent Form</h2>

    {{ form.as_p }}
    <p>
        <label>Email address</label>: {{ user.email }}
    </p>
    <p>
        <label>Date</label>: {{ registration.datetime|time:"g:i A" }} {{ registration.datetime|date:"l j F Y" }}
    </p>


    <p>Thank you,</p>

    <p>The codeWOF team</p>
{% endblock %}
