# Generated by Django 3.2.15 on 2022-08-19 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0012_auto_20220818_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='last_finished',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]