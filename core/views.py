from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from movie.permissions import IsAdminOrReadOnly
from .models import SiteConfiguration
from .permissions import IsSuperUser
from .serializers import (
    SiteConfigurationSerializer,
    UserBriefSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[AllowAny],
        serializer_class=UserRegisterSerializer,
        name="ثبت نام"
    )
    def register(self, request):
        if request.method == "POST":
            serializer = UserRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["GET", "PATCH", "PUT"],
        permission_classes=[IsAuthenticated],
        serializer_class=UserBriefSerializer,
        name="اطلاعات کاربری",
    )
    def me(self, request):
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        if request.method == "GET":
            serializer = UserBriefSerializer(user)
            return Response(serializer.data)
        elif request.method == "PATCH" or request.method == "PUT":
            serializer = UserBriefSerializer(
                user,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data="اطلاعات کاربری با موفقیت تغییر یافت.",
                status=status.HTTP_200_OK,
            )


class SiteConfigurationView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        config = SiteConfiguration.objects.first()
        serializer = SiteConfigurationSerializer(config)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        config = SiteConfiguration.objects.first()
        serializer = SiteConfigurationSerializer(config, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
