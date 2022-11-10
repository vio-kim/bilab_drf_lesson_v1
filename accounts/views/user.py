from django.contrib.auth import logout

from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.permissions import IsOwnerOrIsStaff
from accounts.tasks import send_email_otp_celery
from accounts.models import CustomUser
from accounts.serializers import (
    CustomUserAllFieldsSerializer,
    CustomUserCreateSerializer,
    CustomUserListSerializer,
    CustomUserLoginSerializer,
    CheckUserOTpSerializer
)


class CustomUserViewSet(viewsets.GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserAllFieldsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.action == 'create' or self.action == 'list' or self.action == 'login' \
                or self.action == 'verify_otp':
            permission_classes = [AllowAny]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwnerOrIsStaff]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.action == 'create':
            serializer_class = CustomUserCreateSerializer
        elif self.action == 'list':
            serializer_class = CustomUserListSerializer
        elif self.action == 'login':
            serializer_class = CustomUserLoginSerializer
        elif self.action == 'verify_otp':
            serializer_class = CheckUserOTpSerializer

        return serializer_class

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user_email = serializer.validated_data.get('user').email
        name = serializer.validated_data.get('user').first_name
        surname = serializer.validated_data.get('user').last_name
        otp = serializer.validated_data.get('otp')

        title = 'Test Django otp!'
        message = f'Hello there {name} {surname}!\n OTP: {otp}'
        if otp:
            send_email_otp_celery.delay(user_email, title, message, otp)
            response = {"DETAIL": "OTP was send to user email"}
        else:
            response = CustomUserListSerializer(user).data
            response.__setitem__('tokens', self.get_tokens_for_user(user))

        return Response(data=response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='verify_otp')
    def verify_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = CustomUserListSerializer(serializer.validated_data['user']).data
        response.__setitem__('tokens', self.get_tokens_for_user(serializer.validated_data.get('user')))
        return Response(data=response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='logout')
    def logout(self, request, *args, **kwargs):
        new_tokens = self.get_tokens_for_user(request.user)
        logout(request)
        return Response(data={'DETAIL': "User is Logged Out!"})

    def get_tokens_for_user(self, user: CustomUser):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
