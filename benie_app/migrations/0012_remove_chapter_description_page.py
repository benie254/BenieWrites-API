# Generated by Django 4.1.4 on 2022-12-18 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('benie_app', '0011_alter_story_category_alter_story_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='description',
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='', max_length=5000)),
                ('chapter', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='benie_app.chapter')),
            ],
        ),
    ]
