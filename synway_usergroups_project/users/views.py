from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny

from users.models import CustomUser
from .permissions import IsLoggedInUserOrAdmin
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing, updating and deleting users.
    retrieve:
    Return the given user.
    list:
    Return a list of all the existing users.
    create:
    Create a new user instance.
    delete:
    Delete the user.
    """
    queryset = CustomUser.objects.all().select_related('group')
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        """Set customized permissions."""
        permission_classes = []
        if self.action == 'list' or self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes = [IsLoggedInUserOrAdmin]
        return [permission() for permission in permission_classes]
