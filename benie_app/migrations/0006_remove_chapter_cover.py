# Generated by Django 4.1.4 on 2022-12-16 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('benie_app', '0005_alter_story_tagged'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='cover',
        ),
    ]