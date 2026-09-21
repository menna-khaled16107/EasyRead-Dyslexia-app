from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer
from story.models import Preference

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        x = serializer.save()
        Preference.objects.create(user=x)