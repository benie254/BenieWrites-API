# Generated by Django 4.1.4 on 2023-01-03 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benie_app', '0039_poem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='poem',
            name='cover',
            field=models.URLField(default='', max_length=1000),
        ),
    ]