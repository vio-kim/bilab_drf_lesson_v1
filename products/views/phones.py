from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django_filters import rest_framework as filters

from products.models import Phone
from products.serializers import PhoneAllSerializer, PhoneListSerializer, PhoneRetrieveSerializer, PhoneCreateSerializer
from products.permissions import IsAdminOrReadOnly
from products.filters import PhoneFilterSet


class PhoneViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Phone.objects.all()
    serializer_class = PhoneAllSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = PhoneFilterSet

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.action == 'update' or self.action == 'partial_update' or self.action == 'destroy':
            permission_classes.append(IsAdminOrReadOnly)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == 'list':
            serializer_class = PhoneListSerializer
        elif self.action == 'retrieve':
            serializer_class = PhoneRetrieveSerializer
        elif self.action == 'create':
            serializer_class = PhoneCreateSerializer

        return serializer_class

    def create(self, request, *args, **kwargs):  # POST
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):  # PUT
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
