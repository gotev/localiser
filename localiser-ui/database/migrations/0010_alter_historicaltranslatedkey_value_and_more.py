# Generated by Django 4.1.3 on 2022-11-19 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_alter_historicallocale_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaltranslatedkey',
            name='value',
            field=models.CharField(max_length=2048),
        ),
        migrations.AlterField(
            model_name='translatedkey',
            name='value',
            field=models.CharField(max_length=2048),
        ),
    ]
