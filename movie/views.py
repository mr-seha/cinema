from django.db.models import Count, ExpressionWrapper, F, IntegerField, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django_visit_count.utils import is_new_visit
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import (
    ModelViewSet,
    GenericViewSet
)

from . import serializers
from .filters import CommentFilter, FilmFilter, LinkFilter
from .models import (
    Actor,
    Collection,
    Comment,
    Country,
    Director,
    Film,
    Genre,
    Language,
    Link,
)
from .permissions import IsAdminOrReadOnly, IsAdminOrAuthenticatedOrReadOnly


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='A search term',
            required=False,
            type=str,
        )
    ]
)
@api_view(["GET", "POST"])
@permission_classes([IsAdminOrReadOnly])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.all()
        search_param = request.query_params.get("search")
        if search_param:
            queryset = queryset.filter(title__istartswith=search_param)

        serializer = serializers.CollectionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = serializers.CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, id):
        collection = get_object_or_404(Collection, id=id)
        serializer = serializers.CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        collection = get_object_or_404(Collection, id=id)
        serializer = serializers.CollectionSerializer(
            collection,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, id):
        collection = get_object_or_404(Collection, id=id)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="subtitle",
            type=str,
            required=False,
            description=f"""
            \n- `{Link.SUBTITLE_NO_SUB}` - زیرنویس ندارد
            \n- `{Link.SUBTITLE_PERSIAN_HARD_SUB}` - زیرنویس فارسی چسبیده
            \n- `{Link.SUBTITLE_ENGLISH_HARD_SUB}` - زیرنویس انگلیسی چسبیده
            """,
            enum=[
                Link.SUBTITLE_NO_SUB,
                Link.SUBTITLE_PERSIAN_HARD_SUB,
                Link.SUBTITLE_ENGLISH_HARD_SUB,
            ],
        ),
    ],
)
class FilmViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = FilmFilter
    ordering_fields = [
        "created_date",
        "last_update_date",
        "imdb_rating",
        "visit_count",
    ]
    ordering = ["-last_update_date"]
    search_fields = ["title", "title_en"]
    permission_classes = [IsAdminOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if is_new_visit(request, instance):
            instance.visit_count = F("visit_count") + 1
            instance.save(update_fields=["visit_count"])

        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.FilmSerializer
        return serializers.FilmSavingSerializer

    def get_queryset(self):
        queryset = Film.objects.select_related("director") \
            .prefetch_related(
            "actors",
            "collections",
            "genres",
            "countries",
            "links",
        ).annotate(
            comment_count=Count(
                "comments",
                filter=Q(comments__status=Comment.STATUS_APPROVED)
            ),
        )
        if not self.request.user.is_staff:
            queryset = queryset.filter(status=Film.STATUS_PUBLISHED)

        subtitle = self.request.query_params.get("subtitle")
        if subtitle:
            films = Link.objects.filter(subtitle=subtitle) \
                .values("film").distinct()
            queryset = queryset.filter(id__in=films)

        return queryset

    def get_serializer_context(self):
        return {"user": self.request.user}


class LinkList(ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = serializers.LinkSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LinkFilter
    ordering_fields = ["created_date", "size"]
    permission_classes = [IsAdminUser]


class LinkDetail(RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = serializers.LinkSerializer
    lookup_field = "id"
    permission_classes = [IsAdminUser]


class CommentViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.annotate(
        like=ExpressionWrapper(
            F("like_count") - F("dislike_count"),
            output_field=IntegerField())
    )

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = CommentFilter
    ordering_fields = ["created_date", "rating"]
    search_fields = ["text"]
    permission_classes = [IsAdminUser]

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class CommentNestedViewSet(ModelViewSet):
    serializer_class = serializers.CommentNestedSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["created_date", "like"]
    permission_classes = [IsAdminOrAuthenticatedOrReadOnly]

    @extend_schema(request=None)  # Indicates that the request has no body
    @action(detail=True, methods=["POST"], permission_classes=[AllowAny])
    def like(self, request, **kwargs):
        if request.method == "POST":
            return self._handle_vote(
                "like_count",
                "has_liked",
                error_msg="شما قبلا این نظر را پسند کرده اید"
            )

    @extend_schema(request=None)  # Indicates that the request has no body
    @action(detail=True, methods=["POST"], permission_classes=[AllowAny])
    def dislike(self, request, **kwargs):
        if request.method == "POST":
            return self._handle_vote(
                "dislike_count",
                "has_disliked",
                "شما قبلا این نظر را دیسلایک کرده اید"
            )

    def _handle_vote(self, field_name, key, error_msg):
        obj = self.get_object()

        session_key = f"{key}_comment_{obj.id}"
        if not self.request.session.get(session_key):
            self.request.session[session_key] = True
            setattr(obj, field_name, getattr(obj, field_name) + 1)
            obj.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        film_id = self.kwargs.get("film_pk")
        user = self.request.user

        net_likes = ExpressionWrapper(
            F("like_count") - F("dislike_count"),
            output_field=IntegerField()
        )

        queryset = Comment.objects.filter(film_id=film_id).annotate(
            like=net_likes
        )

        if not user:
            return queryset.filter(status=Comment.STATUS_APPROVED)
        elif user.is_staff:
            return queryset.exclude(status=Comment.STATUS_REJECTED)
        else:
            return queryset.filter(
                Q(status=Comment.STATUS_APPROVED) | Q(user_id=user.id)
            )

    def get_serializer_context(self):
        return {"film_id": self.kwargs.get("film_pk"),
                "user_id": self.request.user.id}


class BaseAttrViewSet(ModelViewSet):
    filter_backends = [SearchFilter]
    permission_classes = [IsAdminOrReadOnly]


class DirectorViewSet(BaseAttrViewSet):
    queryset = Director.objects.all()
    serializer_class = serializers.DirectorSerializer
    search_fields = ["full_name", "full_name_en"]


class ActorViewSet(BaseAttrViewSet):
    queryset = Actor.objects.all()
    serializer_class = serializers.ActorSerializer
    search_fields = ["full_name", "full_name_en"]


class CountryViewSet(BaseAttrViewSet):
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer
    search_fields = ["title"]


class LanguageViewSet(BaseAttrViewSet):
    queryset = Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    search_fields = ["title"]


class GenreViewSet(BaseAttrViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    search_fields = ["title"]
