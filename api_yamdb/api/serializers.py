from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")
        lookup_field = "slug"


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"


class TitlesListSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")

    def validate_year(self, value):
        current_year = datetime.now().year
        if not 0 <= value <= current_year:
            raise serializers.ValidationError(
                "Проверьте год создания произведения"
                "(не может быть больше текущего)."
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UserEmailSerializer(serializers.Serializer):
    username = serializers.SlugField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Нельзя использовать данный username"
            )
        return value


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ("id", "author", "title", "text", "score", "pub_date")
        read_only_fields = ("title",)

    def validate(self, data):
        if self.context["request"].method == "PATCH":
            return data

        title_id = self.context["view"].kwargs.get("title_id")
        user = self.context["request"].user

        is_review_exists = Review.objects.filter(
            title=title_id, author=user
        ).exists()
        if is_review_exists:
            raise serializers.ValidationError("Вы уже оставили отзыв.")
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ("id", "author", "review", "text", "pub_date")
        read_only_fields = ("review",)


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)
