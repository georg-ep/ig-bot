# Generated by Django 3.2.15 on 2022-08-10 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0005_auto_20220805_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_count', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('follow_count', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('unfollow_count', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('comment_count', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('dm_count', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('limits', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='instagram.session')),
            ],
        ),
    ]
