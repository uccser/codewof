# Generated by Django 3.2.6 on 2021-10-26 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0028_programmingconcepts_indent_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(default='programming', max_length=100),
        ),
    ]
