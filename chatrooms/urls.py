from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from . import views

app_name = 'chatrooms'
urlpatterns = [
    url(r'^api/chatrooms/(?P<totp>[0-9]+)$',
        views.ChatroomView.as_view()),
    url(r'^api/chatrooms/', views.TokenValidationView.as_view())
]
