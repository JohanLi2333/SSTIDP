# Generated by Django 4.1.13 on 2024-05-08 16:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dataset", "0003_document_hit_handling_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="directly_return_similarity",
            field=models.FloatField(default=0.9, verbose_name="直接回答相似度"),
        ),
    ]
