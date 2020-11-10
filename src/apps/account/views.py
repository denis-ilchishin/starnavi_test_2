from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserActivityView(APIView):
    def get(self, request: Request):
        return Response(
            {
                "last_login": request.user.last_login,
                "last_activity": request.user.last_activity,
            }
        )
