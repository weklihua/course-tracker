# Generated by Django 4.0.6 on 2022-07-19 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_alter_lesson_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='learning_difference',
            field=models.BooleanField(default=False),
        ),
    ]
