# Generated by Django 5.0.6 on 2024-06-13 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0002_alter_category_options_alter_subtask_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set(),
        ),
    ]
