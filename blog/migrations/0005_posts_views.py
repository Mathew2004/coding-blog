# Generated by Django 4.2.4 on 2023-08-28 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
