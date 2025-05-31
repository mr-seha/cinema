from rest_framework import serializers

from .models import (
    Actor,
    Collection,
    Comment,
    Country,
    Director,
    Film,
    Genre,
    Link,
    Language,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "title"]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["id", "full_name", "full_name_en", "picture"]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "full_name", "full_name_en", "picture"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "title"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "title"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "parent", "user", "text", "rating", "like_count",
                  "dislike_count", "status", "created_date", "film"]

        read_only_fields = ["user", "like_count", "dislike_count"]

    def create(self, validated_data):
        validated_data["user_id"] = self.context.get("user_id")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("film", None)
        return super().update(instance, validated_data)


class CommentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "parent",
            "user",
            "text",
            "rating",
            "like_count",
            "dislike_count",
            "status",
            "created_date",
        ]
        read_only_fields = ["status", "like_count", "dislike_count", "user"]

    def create(self, validated_data):
        film_id = self.context.get("film_id")

        if not Film.objects.filter(id=film_id).exists():
            raise serializers.ValidationError(
                {"film": ["فیلمی با این شناسه یافت نشد"]}
            )

        parent = validated_data.get("parent")
        comments = Film.objects.get(id=film_id).comments.all()
        error_msg = "نظری که به آن پاسخ داده اید در این فیلم وجود ندارد."
        if parent and parent not in comments:
            raise serializers.ValidationError({"parent": [error_msg]})

        validated_data["film_id"] = film_id
        validated_data["user_id"] = self.context.get("user_id")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent admins from changing a comment's parent.
        validated_data.pop("parent", None)
        return super().update(instance, validated_data)


class LinkSerializer(serializers.ModelSerializer):
    languages = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
        many=True,
        label="زبان ها"
    )

    class Meta:
        model = Link
        fields = ["id", "url", "size", "languages", "subtitle", "quality",
                  "season", "episode", "film", "created_date"]


class LinkNestedSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True)

    class Meta:
        model = Link
        fields = [
            "id",
            "url",
            "size",
            "languages",
            "subtitle",
            "quality",
            "season",
            "episode",
        ]


class FilmSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    director = DirectorSerializer()
    genres = CollectionSerializer(many=True)
    collections = CollectionSerializer(many=True)
    actors = ActorSerializer(many=True)
    countries = CountrySerializer(many=True)
    original_languages = LanguageSerializer(many=True)
    links = LinkNestedSerializer(many=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Film
        fields = [
            "id",
            "title",
            "title_en",
            "thumbnail",
            "year",
            "description",
            "is_serial",
            "duration",
            "imdb_rating",
            "imdb_link",
            "status",
            "user",
            "created_date",
            "last_update_date",
            "visit_count",
            "comment_count",
            "director",
            "genres",
            "collections",
            "actors",
            "countries",
            "original_languages",
            "links",
        ]


class FilmSavingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, label="ژانر ها")

    collections = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(),
        many=True,
        required=False,
        label="دسته بندی ها"
    )

    actors = serializers.PrimaryKeyRelatedField(
        queryset=Actor.objects.all(),
        many=True,
        required=False,
        label="بازیگران"
    )

    countries = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), many=True, label="کشور ها"
    )

    original_languages = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), many=True, label="زبان ها"
    )

    class Meta:
        model = Film
        fields = [
            "id",
            "title",
            "title_en",
            "thumbnail",
            "year",
            "description",
            "is_serial",
            "duration",
            "imdb_rating",
            "imdb_link",
            "status",
            "user",
            "created_date",
            "last_update_date",
            "director",
            "genres",
            "collections",
            "actors",
            "countries",
            "original_languages",
        ]

    def validate_countries(self, countries):
        if not countries:
            error_msg = "لطفا حداقل یک کشور برای فیلم انتخاب کنید."
            if Country.objects.count() == 0:
                error_msg += " ابتدا از بخش کشور ها یک کشور اضافه نمایید."
            raise serializers.ValidationError([error_msg])
        return countries

    def validate_genres(self, genres):
        if not genres:
            error_msg = "لطفا حداقل یک ژانر برای فیلم انتخاب کنید."
            if Genre.objects.count() == 0:
                error_msg += " ابتدا از بخش ژانر ها یک ژانر اضافه نمایید."
            raise serializers.ValidationError([error_msg])
        return genres

    def create(self, validated_data):
        validated_data["user"] = self.context["user"]
        return super().create(validated_data)
