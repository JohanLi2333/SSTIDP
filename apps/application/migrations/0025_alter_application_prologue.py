# Generated by Django 4.2.18 on 2025-01-22 09:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0024_applicationaccesstoken_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="prologue",
            field=models.CharField(default="", max_length=40960, verbose_name="开场白"),
        ),
    ]
