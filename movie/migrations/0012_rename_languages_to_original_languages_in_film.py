# Generated by Django 5.2.1 on 2025-05-23 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0011_refactor_language_to_languages_m2m_in_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='film',
            old_name='languages',
            new_name='original_languages',
        ),
    ]
