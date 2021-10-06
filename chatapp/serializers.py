from django.contrib.auth import models
from django.contrib.auth.models import User
from rest_framework import serializers
from chatapp.models import Message, Channel, ChannelMessage, ChannelMembership


class ChannelUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ['name', 'description', 'created', 'updated']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    channels = ChannelUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'channels',)


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name')


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(
        many=False, slug_field='username', queryset=User.objects.all())
    receiver = serializers.SlugRelatedField(
        many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'created', 'read', 'message']


class ChannelSerializer(serializers.ModelSerializer):
    members = ShortUserSerializer(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = ['name', 'description', 'members', 'created', 'updated']


class ShortChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ['name', 'created', 'updated']


class ChannelMessageSerializer(serializers.ModelSerializer):
    sender = ShortUserSerializer()
    channel = ShortChannelSerializer()

    class Meta:
        model = ChannelMessage
        fields = ['message', 'sender', 'channel', 'created']


class ChannelMembershipSerializer(serializers.ModelSerializer):
    channel_user = UserSerializer()
    member_channel = ChannelSerializer(many=True, read_only=True)

    class Meta:
        model = ChannelMembership
        fields = ['first_name', 'channel_user', 'member_channel', 'created']
