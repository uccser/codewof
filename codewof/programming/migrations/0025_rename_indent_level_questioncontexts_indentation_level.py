# Generated by Django 3.2.6 on 2021-10-07 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0024_auto_20211007_1412'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questioncontexts',
            old_name='indent_level',
            new_name='indentation_level',
        ),
    ]