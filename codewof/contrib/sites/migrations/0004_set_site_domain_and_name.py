"""
To understand why this file is here, please read:

http://cookiecutter-django.readthedocs.io/en/latest/faq.html#why-is-there-a-django-contrib-sites-directory-in-cookiecutter-django
"""
from django.conf import settings
from django.db import migrations


def update_site_forward(apps, schema_editor):
    """Set site domain and name."""
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        id=settings.SITE_ID,
        defaults={
            "domain": "codewof.co.nz",
            "name": "codewof",
        },
    )


class Migration(migrations.Migration):

    dependencies = [("sites", "0003_set_site_domain_and_name")]

    operations = [migrations.RunPython(update_site_forward)]
