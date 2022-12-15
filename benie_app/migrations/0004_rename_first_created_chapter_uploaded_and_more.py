# Generated by Django 4.1.4 on 2022-12-15 10:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('benie_app', '0003_chapter_first_created_chapter_last_updated_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chapter',
            old_name='first_created',
            new_name='uploaded',
        ),
        migrations.RenameField(
            model_name='story',
            old_name='first_created',
            new_name='uploaded',
        ),
        migrations.AddField(
            model_name='chapter',
            name='first_published',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='story',
            name='first_published',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
