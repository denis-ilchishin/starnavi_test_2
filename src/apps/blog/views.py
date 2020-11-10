from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from . import serializers
from .models import Post, PostLike


class PostCreateView(CreateAPIView):
    serializer_class = serializers.PostCreateSerializer


class PostLikeView(APIView):
    def post(self, request: Request, pk):

        # Return 404 if post not found
        if not Post.objects.filter(pk=pk).exists():
            return Http404()

        # Raise ValidatorError if current user already liked this post
        if request.user.post_likes.filter(post=pk).exists():
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: [_("You already likes this post")]}
            )

        PostLike.objects.create(user=request.user, post_id=pk)

        return Response(None, status=HTTP_204_NO_CONTENT)


class PostUnlikeView(APIView):
    def post(self, request: Request, pk):

        # Return 404 if post not found
        if not Post.objects.filter(pk=pk).exists():
            return Http404()

        # Raise ValidatorError if current user haven't likes this post yet
        try:
            post_like = request.user.post_likes.get(post=pk)
        except ObjectDoesNotExist:
            raise ValidationError(
                {
                    api_settings.NON_FIELD_ERRORS_KEY: [
                        _("You haven't liked this post yet")
                    ]
                }
            )

        post_like.delete()

        return Response(None, status=HTTP_204_NO_CONTENT)
