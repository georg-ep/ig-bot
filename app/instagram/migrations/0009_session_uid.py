# Generated by Django 3.2.15 on 2022-08-10 10:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0008_auto_20220810_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
