# Generated by Django 4.2.1 on 2023-06-10 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0006_increase_name_max_length'),
        ('user', '0004_rename_fqa_faq'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='currencies.currency'),
        ),
    ]
