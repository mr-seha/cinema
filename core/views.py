from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permissions import IsSuperUser
from .serializers import UserSerializer, UserBriefSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated],
            serializer_class=UserBriefSerializer, name='اطلاعات کاربری')
    def me(self, request):
        user = get_object_or_404(get_user_model(), pk=request.user.pk)
        if request.method == 'GET':
            serializer = UserBriefSerializer(user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = UserBriefSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response("اطلاعات کاربری با موفقیت تغییر یافت.", status=status.HTTP_200_OK)
