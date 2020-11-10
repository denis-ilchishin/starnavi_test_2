from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView  # TokenRefreshView,

app_name = "authentication"

urlpatterns = (
    path("token/", TokenObtainPairView.as_view(), name="signin"),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'), # TODO: add refresh route token
)
