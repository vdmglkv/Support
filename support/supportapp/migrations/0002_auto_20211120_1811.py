# Generated by Django 3.2.9 on 2021-11-20 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supportapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='answer',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='ticket',
            name='from_user',
            field=models.EmailField(default='Unknown', max_length=255),
        ),
    ]
