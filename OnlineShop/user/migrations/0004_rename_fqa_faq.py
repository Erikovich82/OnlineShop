# Generated by Django 4.2.1 on 2023-06-10 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_fqa'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FQA',
            new_name='FAQ',
        ),
    ]