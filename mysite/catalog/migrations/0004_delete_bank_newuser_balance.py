# Generated by Django 4.0.5 on 2022-07-06 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_bank'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bank',
        ),
        migrations.AddField(
            model_name='newuser',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=True, max_digits=5),
        ),
    ]
