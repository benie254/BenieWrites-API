# Generated by Django 4.1.4 on 2022-12-18 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benie_app', '0014_alter_chapter_story_alter_page_chapter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='category',
            field=models.CharField(choices=[('mystery', 'mystery'), ('thriller', 'thriller'), ('drama', 'drama'), ('mystery/thriller', 'mystery/thriller'), ('action', 'action'), ('romance', 'romance'), ('teen-fiction', 'teen-fiction')], default='', max_length=60),
        ),
    ]