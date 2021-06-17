# Generated by Django 3.2.4 on 2021-06-17 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountmodel',
            name='imap_port',
            field=models.IntegerField(default=143),
        ),
        migrations.AddField(
            model_name='accountmodel',
            name='root_mailbox',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='accountmodel',
            name='smtp_port',
            field=models.IntegerField(default=465),
        ),
        migrations.AddField(
            model_name='accountmodel',
            name='sub_mailboxes',
            field=models.CharField(default='N/A', max_length=400),
        ),
    ]
