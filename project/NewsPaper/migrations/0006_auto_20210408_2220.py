# Generated by Django 3.1.7 on 2021-04-08 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NewsPaper', '0005_auto_20210408_0729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='username',
            new_name='user',
        ),
    ]
