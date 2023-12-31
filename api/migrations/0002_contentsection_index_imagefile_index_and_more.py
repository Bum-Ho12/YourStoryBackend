# Generated by Django 4.2.7 on 2023-12-04 10:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentsection',
            name='index',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1000)]),
        ),
        migrations.AddField(
            model_name='imagefile',
            name='index',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1000)]),
        ),
        migrations.AlterField(
            model_name='blog',
            name='frontImage',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
