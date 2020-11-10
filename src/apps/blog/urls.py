from django.urls import path
from django.urls.conf import include

from . import views

app_name = "blog"

urlpatterns = (
    path(
        "posts/",
        include(
            (
                (
                    path("create/", views.PostCreateView.as_view(), name="create"),
                    path("like/<int:pk>/", views.PostLikeView.as_view(), name="like"),
                    path(
                        "unlike/<int:pk>/",
                        views.PostUnlikeView.as_view(),
                        name="unlike",
                    ),
                ),
                "posts",
            )
        ),
    ),
)
