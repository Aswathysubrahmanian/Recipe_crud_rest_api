# Generated by Django 4.0.5 on 2023-10-09 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipeapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
    ]
