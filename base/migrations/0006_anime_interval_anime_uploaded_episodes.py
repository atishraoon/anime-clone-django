# Generated by Django 5.1.4 on 2024-12-21 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_anime_total_episodes_alter_episode_episode_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='interval',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='anime',
            name='uploaded_episodes',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
