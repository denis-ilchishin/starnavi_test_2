from rest_framework import generics

from . import serializers


class PostCreateView(generics.CreateAPIView):
    serializer_class = serializers.PostCreateSerializer
