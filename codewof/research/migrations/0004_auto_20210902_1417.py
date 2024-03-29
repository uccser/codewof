# Generated by Django 3.2.6 on 2021-09-02 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0003_study_researchers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studygroup',
            name='questions',
        ),
        migrations.RemoveField(
            model_name='studygroup',
            name='study',
        ),
        migrations.RemoveField(
            model_name='studyregistration',
            name='study_group',
        ),
        migrations.AlterField(
            model_name='studyregistration',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='Study',
        ),
        migrations.DeleteModel(
            name='StudyGroup',
        ),
    ]
