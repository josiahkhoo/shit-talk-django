from rest_framework import serializers
from .models import Chatroom
from django.contrib.auth import authenticate


class ChatroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chatroom
        fields = ('id', 'key', 'datetime_created', 'is_active')
