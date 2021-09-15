# Generated by Django 3.2.6 on 2021-09-13 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programming', '0014_difficultylevel_programmingconcepts_questioncontext'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='difficulty_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='programming.difficultylevel'),
        ),
    ]