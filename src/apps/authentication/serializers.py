from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DefaultValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=get_user_model()
        ._meta.get_field(get_user_model().USERNAME_FIELD)
        .validators
    )
    email = serializers.EmailField(
        validators=get_user_model()
        ._meta.get_field(get_user_model().EMAIL_FIELD)
        .validators
    )
    password = serializers.CharField()
    password_confirm = serializers.CharField()

    def validate(self, attrs):
        """
        We want to integrate build-in django password validation into our DRF serializer.

        To make it work it requires an user instance, because validation may based
            on user's other attributes such as `UserAttributeSimilarityValidator`.

        Since here we are registring a !new! user, we don't have the user instance yet, so we emulating it
            based on serializer data and only then perform django build-in password validation
        """

        password_confirm = attrs.get("password_confirm")

        # remove `password_confirm` from `attrs` dict for later convience
        del attrs["password_confirm"]

        user = get_user_model()(**attrs)

        password = attrs.get("password")

        try:
            validate_password(password=password, user=user)
        except DefaultValidationError as e:
            raise ValidationError({"password": list(e.messages)})

        if password_confirm != password:
            raise ValidationError(
                {"password_confirm": (_("Passwords must be the same"),)}
            )

        return super().validate(attrs)
