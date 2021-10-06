# Generated by Django 3.2.7 on 2021-10-06 04:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatapp', '0002_channel_channelmembership_channelmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='description',
            field=models.CharField(default='Test Description', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channel',
            name='members',
            field=models.ManyToManyField(related_name='channels', through='chatapp.ChannelMembership', to=settings.AUTH_USER_MODEL),
        ),
    ]
