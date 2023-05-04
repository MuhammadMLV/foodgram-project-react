from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CreateDeleteViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    pass
