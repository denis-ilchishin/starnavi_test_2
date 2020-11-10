from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post, PostLike


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


class PostsLikeTests(APITestCase):
    """
    In the real world we probably don't want to give users access to like theirs posts.
    But right now for simplicity we don't mind
    """

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="some-user", password="some-password"
        )
        self.post = Post.objects.create(user=self.user, text="some post's text")

    def test_post_like(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse("blog:posts:like", kwargs={"pk": self.post.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PostLike.objects.count(), 1)
        self.assertEqual(PostLike.objects.get().user, self.user)
        self.assertEqual(PostLike.objects.get().post, self.post)

    def test_post_unlike(self):
        self.client.force_authenticate(user=self.user)

        PostLike.objects.create(user=self.user, post=self.post)

        response = self.client.post(
            reverse("blog:posts:unlike", kwargs={"pk": self.post.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PostLike.objects.count(), 0)
