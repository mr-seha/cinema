from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .validators import password_validator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'is_staff', 'is_active',
                  'date_joined', 'email', 'groups', 'user_permissions']

        read_only_fields = ['date_joined', 'last_login']


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'last_login', 'username', 'password', 'first_name', 'last_name', 'email']

        read_only_fields = ['last_login']

    password = serializers.CharField(max_length=255, write_only=True,
                                     style={'input_type': 'password'}, validators=[password_validator])

    def save(self, **kwargs):
        self.validated_data['password'] = make_password(self.validated_data['password'])
        super().save()
