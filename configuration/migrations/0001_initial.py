# Generated by Django 3.2.4 on 2021-06-15 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChecksModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'checks',
            },
        ),
    ]
