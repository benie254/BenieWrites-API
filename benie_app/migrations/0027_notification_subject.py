# Generated by Django 4.1.4 on 2022-12-19 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benie_app', '0026_remove_notification_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='subject',
            field=models.CharField(blank=True, default='', max_length=60, null=True),
        ),
    ]
