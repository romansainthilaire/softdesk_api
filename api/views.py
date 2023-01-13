from django.shortcuts import render

from rest_framework import generics

from api.serializers import UserSerializer


class SignupView(generics.CreateAPIView):

    serializer_class = UserSerializer
