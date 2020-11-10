from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # TokenRefreshView,

from . import views

app_name = "authentication"

urlpatterns = (
    path("token/", TokenObtainPairView.as_view(), name="signin"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    # TODO: add refresh token route
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
)
