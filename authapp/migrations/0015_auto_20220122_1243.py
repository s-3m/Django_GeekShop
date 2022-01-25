# Generated by Django 3.2.11 on 2022-01-22 09:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0014_merge_0003_alter_shopuser_age_0013_auto_20220118_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 24, 9, 43, 17, 145453, tzinfo=utc), verbose_name='Истечение срока активации'),
        ),

    ]
