# Generated by Django 4.2.15 on 2024-09-13 18:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0013_application_tts_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="problem_optimization_prompt",
            field=models.CharField(
                blank=True,
                default="()里面是用户问题,根据上下文回答揣测用户问题({question}) 要求: 输出一个补全问题,并且放在<data></data>标签中",
                max_length=102400,
                null=True,
                verbose_name="问题优化提示词",
            ),
        ),
    ]
