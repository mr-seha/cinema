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

    password = serializers.CharField(max_length=255,
                                     write_only=True,
                                     allow_blank=True,
                                     help_text="برای عدم تغییر پسورد فیلد را خالی بگذارید.",
                                     style={'input_type': 'password'},
                                     validators=[password_validator]
                                     )

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
