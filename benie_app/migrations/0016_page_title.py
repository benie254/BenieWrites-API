# Generated by Django 4.1.4 on 2022-12-18 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benie_app', '0015_alter_story_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='title',
            field=models.CharField(default='', max_length=120),
        ),
    ]