# Generated by Django 3.2.15 on 2022-08-10 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0010_auto_20220810_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionlimit',
            name='session',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='limits', to='instagram.session'),
        ),
    ]
