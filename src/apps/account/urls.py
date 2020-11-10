from django.urls import path
from django.urls.conf import include

from . import views

app_name = "account"

urlpatterns = (
    path(
        "activity/",
        views.UserActivityView.as_view(),
        name='user-activity'
    ),
)
