from django.conf import settings
from django.db import models
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from cent import Client
# Django Build in User Model
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from chatapp.models import ChannelMessage, Channel, ChannelMembership
from chatapp.serializers import ChannelSerializer, MessageSerializer, UserSerializer, ChannelMessageSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            try:
                channel = Channel.objects.get(name='Welcome')
            except Channel.DoesNotExist:
                channel = Channel.objects.create(name='Welcome')
            membership = ChannelMembership.objects.create(
                user=user, channel=channel)
            token_dict = {'token': token.key}
            token_dict.update(serializer.data)
            return Response(token_dict, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], url_path='join-channel')
    def join_channel(self, request):
        user = request.user
        channel_query = request.query_params.get('channel', None)
        try:
            channel = Channel.objects.get(name__iexact=channel_query)
        except Channel.DoesNotExist:
            return Response({'error': "Channel Does Not Exist"}, status=400)

        membership = ChannelMembership.objects.get_or_create(
            user=user, channel=channel)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['get'], url_path='channel-messages')
    def channel_messages(self, request):
        user = request.user
        channel_query = request.query_params.get('channel', None)
        try:
            channel = Channel.objects.get(name__iexact=channel_query)
        except Channel.DoesNotExist:
            return Response({'error': f"Channel {channel_query} does not exist"}, status=400)

        try:
            membership = ChannelMembership.objects.get(
                user=user, channel=channel)
        except ChannelMembership.DoesNotExist:
            return Response({'error': f'User {user.username} does not belong to the channel {channel.name}'})
        messages = ChannelMessage.objects.filter(sender=user, channel=channel)
        serializer = ChannelMessageSerializer(messages, many=True)
        return Response({'data': serializer.data}, status=200)

    @action(methods=['post'], detail=False, url_path='chat')
    def send_channel_message(self, request):
        user = request.user
        channel_query = request.query_params.get('channel', None)
        try:
            channel = Channel.objects.get(name__iexact=channel_query)
        except Channel.DoesNotExist:
            return Response({'error': f"Channel {channel_query} does not exist"}, status=400)

        try:
            membership = ChannelMembership.objects.get(
                user=user, channel=channel)
        except ChannelMembership.DoesNotExist:
            return Response({'error': f'User {user.username} does not belong to the channel {channel.name}'})
        message_data = request.data.get('message', None)
        if message_data:
            message = ChannelMessage.objects.create(
                sender=user, channel=channel, message=message_data)
            messages = ChannelMessage.objects.filter(
                sender=user, channel=channel)
            serializer = ChannelMessageSerializer(messages, many=True)
            return Response({'data': serializer.data}, status=200)
        return Response({'error': 'None or empty messages are not accepted'})


class ChannelViewSet(ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ChannelMessageViewSet(ModelViewSet):
    queryset = ChannelMessage.objects.all()
    serializer_class = ChannelMessageSerializer

# @csrf_exempt
# def message_list(request, sender=None, receiver=None):
#     """
#     List all required messages, or create a new message.
#     """
#     if request.method == 'GET':
#         messages = Message.objects.filter(
#             sender_id=sender, receiver_id=receiver)
#         serializer = MessageSerializer(
#             messages, many=True, context={'request': request})
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = MessageSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
