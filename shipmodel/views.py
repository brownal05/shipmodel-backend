from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from shipmodel.src.api import ShipModelAPI
from .models import Vsl
from .serializers import VslSerializer
from rest_framework import viewsets

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
        vsl = [vsl.vessel for vsl in Vsl.objects.all()]
        return Response(vsl)

    def post(self, request, format=None):
        """
        perform calculation based user inputs
        """
        apiHandler = ShipModelAPI()

        usernames = [user.username for user in User.objects.all()]
        return Response({'result':apiHandler.perform_calculation(request.data)})

class VslViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Vsl.objects.all().order_by('-id')
    serializer_class = VslSerializer
