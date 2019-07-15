"""ViewSets for groups application."""
from django.db.models import ProtectedError
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Group
from .serializers import GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    retrieve:
    Return the given group.
    list:
    Return a list of all the existing groups.
    create:
    Create a new group.
    delete:
    Delete the group.
    """
    queryset = Group.objects.all().prefetch_related('users')
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except ProtectedError:
            raise ValidationError(
                "Can't delete group with users."
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
