# Generated by Django 3.2.15 on 2022-08-10 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0009_session_uid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sessionlimit',
            old_name='limits',
            new_name='session',
        ),
        migrations.AlterField(
            model_name='session',
            name='status',
            field=models.CharField(choices=[('Running', 'Running'), ('Not Started', 'Not Started'), ('Finished', 'Finished'), ('Error', 'Error'), ('Cancelled', 'Cancelled')], default='Not Started', max_length=255),
        ),
    ]
