# Generated by Django 3.1 on 2020-08-12 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_auto_20200812_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='difficulty',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='word',
            name='language',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
