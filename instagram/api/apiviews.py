from django.shortcuts import render
from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth.models import User

# Create your views here.

class UserApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailedApiView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer