# Generated by Django 3.2.4 on 2021-07-12 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_taskmodel_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='range',
            field=models.CharField(default='(UNSEEN)', max_length=50),
        ),
    ]
