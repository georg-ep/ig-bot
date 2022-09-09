# Generated by Django 3.2.15 on 2022-08-23 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0017_auto_20220823_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='status',
            field=models.CharField(choices=[('Running', 'Running'), ('Idle', 'Idle'), ('Excluded', 'Excluded')], default='Idle', max_length=255),
        ),
        migrations.AlterField(
            model_name='session',
            name='status',
            field=models.CharField(choices=[('Running', 'Running'), ('Finished', 'Finished'), ('Error', 'Error')], default='Running', max_length=255),
        ),
    ]