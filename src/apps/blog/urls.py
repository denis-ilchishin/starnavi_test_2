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
                    # path(views.PostLike.as_view(), name="like"),
                    # path(views.PostUnlike.as_view(), name="unlike"),
                ),
                "posts",
            )
        ),
    ),
)
