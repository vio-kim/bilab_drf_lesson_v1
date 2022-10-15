from rest_framework import serializers

from accounts.models import CustomUser


class CustomUserAllFieldsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = 'first_name', 'last_name', 'phone', 'email', 'iin'


class CustomUserListSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format='%d-%m-%y %H:%M')

    class Meta:
        model = CustomUser
        fields = 'uuid', 'first_name', 'last_name', \
                 'phone', 'email', 'iin', 'last_login', \
                 'is_active', 'role'
