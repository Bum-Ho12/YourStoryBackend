# Generated by Django 4.2.7 on 2023-12-17 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_blog_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='contentImage',
            field=models.ManyToManyField(blank=True, to='api.imagefile'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blog',
            name='story',
            field=models.ManyToManyField(blank=True, to='api.contentsection'),
        ),
    ]
