# Generated by Django 4.1.4 on 2022-12-18 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benie_app', '0010_story_author_alter_story_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='category',
            field=models.CharField(choices=[('mystery', 'mystery'), ('thriller', 'thriller'), ('drama', 'drama'), ('mystery/thriller', 'mystery/thriller'), ('action', 'action'), ('romance', 'romance')], default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='story',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('ongoing', 'ongoing')], default='', max_length=60),
        ),
    ]