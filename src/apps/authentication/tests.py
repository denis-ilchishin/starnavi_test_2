from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def test_signup(self):
        username = "some-username-example"
        email = "some-mail@example.com"
        password = password_confirm = "some-password-example"

        data = {
            "username": username,
            "email": email,
            "password": password,
            "password_confirm": password_confirm,
        }

        response = self.client.post(reverse("authentication:signup"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().username, username)
        self.assertEqual(get_user_model().objects.get().email, email)

    def test_signin(self):
        username = "some-username-example"
        password = "some-password-example"

        user = get_user_model().objects.create_user(
            username=username, password=password
        )

        data = {"username": username, "password": password}

        response = self.client.post(reverse("authentication:signin"), data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
