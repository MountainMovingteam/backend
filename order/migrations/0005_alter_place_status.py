# Generated by Django 5.0 on 2024-04-28 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0004_alter_place_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="place",
            name="status",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
