# Generated by Django 3.2.11 on 2022-01-16 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_alter_shopuser_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='age',
            field=models.PositiveIntegerField(default=18, null=True, verbose_name='Возраст'),
        ),
    ]
