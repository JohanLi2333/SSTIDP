# Generated by Django 4.2.15 on 2025-01-06 10:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0022_application_tts_autoplay"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="stt_autosend",
            field=models.BooleanField(default=False, verbose_name="自动发送"),
        ),
    ]
