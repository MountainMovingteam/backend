# Generated by Django 5.0 on 2024-04-27 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_alter_order_table_alter_place_table_alter_team_table_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="status",
            field=models.IntegerField(blank=True),
        ),
    ]
