from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from story.models import Preference

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        x = serializer.save()
        Preference.objects.create(user=x)



class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:

            x = RefreshToken(request.data["refresh"])
            x.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        