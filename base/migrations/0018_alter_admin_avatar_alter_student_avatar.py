# Generated by Django 5.0 on 2024-05-01 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0017_admin_academy_admin_phone_alter_admin_avatar_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admin",
            name="avatar",
            field=models.FileField(blank=True, null=True, upload_to="images/"),
        ),
        migrations.AlterField(
            model_name="student",
            name="avatar",
            field=models.FileField(blank=True, null=True, upload_to="images/"),
        ),
    ]
