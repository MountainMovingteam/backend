# Generated by Django 4.1.3 on 2024-04-26 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0003_alter_order_table_alter_place_table_alter_team_table_and_more"),
        ("manager", "0002_alter_lecturer_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="LecturePlace",
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
                (
                    "lecture",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="manager.lecturer",
                    ),
                ),
                (
                    "place",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="order.place"
                    ),
                ),
            ],
            options={
                "db_table": "LecturePlace",
            },
        ),
    ]
