# Generated by Django 5.1.1 on 2024-10-04 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_remove_toy_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='toys',
            field=models.ManyToManyField(to='main_app.toy'),
        ),
    ]
