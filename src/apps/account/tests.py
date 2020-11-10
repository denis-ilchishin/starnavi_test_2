from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def setUp(self) -> None:
        self.username = "some-username"
        self.password = "some-password"

        self.user = get_user_model().objects.create_user(
            username=self.username, password=self.password
        )

    def test_user_last_login(self):
        data = {"username": self.username, "password": self.password}

        self.assertEqual(self.user.last_login, None)

        response = self.client.post(reverse("authentication:signin"), data)

        self.user.refresh_from_db()

        self.assertAlmostEqual(
            self.user.last_login.timestamp(), timezone.now().timestamp(), places=1
        )

    def test_user_last_activity(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse("blog:posts:create"), {"text": "some post text here"}
        )

        self.user.refresh_from_db()

        self.assertAlmostEqual(
            self.user.last_activity.timestamp(), timezone.now().timestamp(), places=1
        )

    def test_user_activity_endpoint(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse("account:user-activity"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
