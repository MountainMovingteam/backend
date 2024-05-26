# Generated by Django 4.1.3 on 2024-05-26 12:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=1000)),
                ("A_content", models.CharField(max_length=200)),
                ("B_content", models.CharField(max_length=200)),
                ("C_content", models.CharField(max_length=200)),
                ("D_content", models.CharField(max_length=200)),
                (
                    "answer",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(15),
                        ]
                    ),
                ),
                ("type", models.IntegerField()),
            ],
            options={
                "db_table": "Question",
            },
        ),
    ]
