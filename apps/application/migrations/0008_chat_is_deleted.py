# Generated by Django 4.1.13 on 2024-06-13 11:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0007_alter_application_prologue"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat",
            name="is_deleted",
            field=models.BooleanField(default=False, verbose_name=""),
        ),
    ]
