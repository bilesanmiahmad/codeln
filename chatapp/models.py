from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1000)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.message

    class Meta:
        ordering = ('created',)


class Channel(models.Model):
    name = models.CharField('Channel Name', max_length=20)
    description = models.CharField(max_length=300)
    members = models.ManyToManyField(
        User, related_name='channels', through='ChannelMembership', through_fields=('channel', 'user',))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('created',)


class ChannelMessage(models.Model):
    message = models.CharField(max_length=500)
    sender = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='send_user')
    channel = models.ForeignKey(
        Channel, on_delete=models.DO_NOTHING, related_name='channel')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.message} -- {self.sender.email}'

    class Meta:
        ordering = ('created',)


class ChannelMembership(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='channel_user')
    channel = models.ForeignKey(
        Channel, on_delete=models.DO_NOTHING, related_name='member_channel')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.channel} -- {self.user.username}'

    class Meta:
        ordering = ('created',)
