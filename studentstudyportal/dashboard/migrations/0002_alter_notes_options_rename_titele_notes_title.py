# Generated by Django 5.0 on 2023-12-12 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notes',
            options={'verbose_name': 'notes', 'verbose_name_plural': 'notes'},
        ),
        migrations.RenameField(
            model_name='notes',
            old_name='titele',
            new_name='title',
        ),
    ]
