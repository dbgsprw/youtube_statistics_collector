# Generated by Django 2.2.2 on 2019-06-28 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20190627_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.URLField(null=True),
        ),
    ]
