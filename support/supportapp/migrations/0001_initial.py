# Generated by Django 3.2.9 on 2021-11-28 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(blank=True, max_length=300)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.CharField(default='Unknown', max_length=255)),
                ('support_answer', models.CharField(default='None', max_length=255)),
                ('user_answer', models.CharField(default='None', max_length=255)),
                ('status', models.CharField(choices=[('Resolved', 'Resolved'), ('Unresolved', 'Unresolved'), ('Frozen', 'Frozen')], default='Unresolved', max_length=10)),
            ],
        ),
    ]
