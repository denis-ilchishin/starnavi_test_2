from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post


class PostTests(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="some-user", password="some-password"
        )

    def test_post_creation(self):
        self.client.force_authenticate(user=self.user)

        data = {"text": "some post text here"}

        response = self.client.post(reverse("blog:posts:create"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.get().text, data["text"])
        self.assertEqual(Post.objects.get().user, self.user)
