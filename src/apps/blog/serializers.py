from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ("user", "text")


class PostAnalyticsQuerySerializers(serializers.Serializer):
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    def validate(self, attrs):
        if attrs.get("date_from") >= attrs.get("date_to"):
            raise ValidationError(
                {"date_from": [_("`date_from` value must be lower that `date_to`")]}
            )

        return attrs
