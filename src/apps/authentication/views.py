from django.contrib.auth import get_user_model
from django.http import request
from rest_framework import generics, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .serializers import SignupSerializer


class SignupView(generics.GenericAPIView):
    permission_classes = (~permissions.IsAuthenticated,)
    serializer_class = SignupSerializer

    def post(self, request: Request, **kwargs):
        serializer: SignupSerializer = self.get_serializer(data=request.data)

        serializer.is_valid(True)

        data = serializer.validated_data

        user = get_user_model().objects.create_user(**data)

        # TODO: here we probably want to return serialized user data or jwt token to prevent client to make one more request to obtain it
        return Response(None, status=HTTP_201_CREATED)
