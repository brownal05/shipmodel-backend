from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from shipmodel.src.api import ShipModelAPI

class ListCalculator(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)

    def post(self, request, format=None):
        """
        perform calculation based user inputs
        """
        apiHandler = ShipModelAPI()

        usernames = [user.username for user in User.objects.all()]
        return Response({'result':apiHandler.perform_calculation(request.data)})