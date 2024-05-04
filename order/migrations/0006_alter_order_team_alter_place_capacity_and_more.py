from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_place_capacity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.team'),
        ),
        migrations.AlterField(
            model_name='place',
            name='capacity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='place',
            name='status',

            field=models.IntegerField(blank=True, null=True),
        ),
    ]
