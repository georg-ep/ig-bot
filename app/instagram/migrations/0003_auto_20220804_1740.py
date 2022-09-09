# Generated by Django 3.2.15 on 2022-08-04 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0002_session'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='client_type',
        ),
        migrations.AddField(
            model_name='session',
            name='session_type',
            field=models.CharField(choices=[('Follow', 'Follow'), ('Like Follow', 'Like Follow')], default='Follow', max_length=255),
        ),
    ]
