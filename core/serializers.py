from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import SiteConfiguration


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "email",
            "groups",
            "user_permissions",
        ]

        read_only_fields = ["date_joined", "last_login"]


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "last_login",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        ]
        read_only_fields = ["last_login"]

    password = serializers.CharField(
        max_length=255,
        write_only=True,
        required=False,
        help_text="برای عدم تغییر پسورد فیلد را خالی بگذارید.",
        style={"input_type": "password"},
        label="رمز عبور"
    )

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        user = super().update(instance, validated_data)
        if password:
            try:
                validate_password(password, user=user)
            except DjangoValidationError as errors:
                raise serializers.ValidationError({"password": list(errors)})

            user.set_password(password)
            user.save()

        return user


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "email",
            "password",
            "confirm_password",
        ]

    password = serializers.CharField(
        max_length=255,
        write_only=True,
        style={"input_type": "password"},
        label="رمز عبور"
    )

    confirm_password = serializers.CharField(
        max_length=255,
        write_only=True,
        style={"input_type": "password"},
        label="تکرار رمز عبور"
    )

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        confirm_password = validated_data.pop("confirm_password", None)

        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": ["رمز عبور و تکرار آن با یکدیگر مطابقت ندارند."]}
            )

        user = get_user_model()(**validated_data)

        try:
            validate_password(password, user=user)
        except DjangoValidationError as errors:
            raise serializers.ValidationError({"password": list(errors)})

        user.set_password(password)
        user.save()

        return user


class SiteConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteConfiguration
        fields = [
            "site_title",
            "telegram_channel",
            "instagram_page",
            "phone_number",
            "copyright_text",
        ]
