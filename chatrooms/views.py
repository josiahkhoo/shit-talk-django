from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status, authentication, permissions
from pyotp import TOTP
import jwt
import base64

from .serializers import ChatroomSerializer
from .models import *
from .backends import JWTAuthentication
from shit_talk.settings import SECRET_KEY


class ChatroomView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, totp):
        chatrooms = Chatroom.objects.all()
        for chatroom in chatrooms:
            salt = chatroom.salt
            validator = TOTP(salt)
            if validator.verify(totp):
                data = ChatroomSerializer(chatroom).data
                token = jwt.encode(data, SECRET_KEY)
                body = {"token": token}
                body.update(serializer_to_body(
                    ChatroomSerializer, chatroom, "chatroom"))
                return Response(body, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)


class TokenValidationView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        return JWTAuthentication.authenticate(request)


def serializer_to_body(serializer, obj, obj_name):
    data = dict()
    data[obj_name] = serializer(obj).data
    return {'data': data}


def post_request_parser(request):
    """
    converts POST requests into appropriate form data:
    json -> form
    form -> form
    """
    if request.META["CONTENT_TYPE"] == "application/json":
        data = jsonForm(request)
    else:
        data = request.POST
    return data
