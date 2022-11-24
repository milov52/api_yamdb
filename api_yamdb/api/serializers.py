from datetime import datetime

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator

from reviews.models import Categories, Genres, Titles, User, Reviews, Comments


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ("name", "slug")
        lookup_field = "slug"


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ("name", "slug")
        lookup_field = "slug"


class TitlesListSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)

    class Meta:
        model = Titles
        fields = ("id", "name", "year", "rating", "description", "genre", "category")


class TitlesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genres.objects.all()
    )

    class Meta:
        model = Titles
        fields = ("id", "name", "year", "rating", "description", "genre", "category")

    def validate_year(self, value):
        current_year = datetime.now().year
        if not 0 <= value <= current_year:
            raise serializers.ValidationError(
                "Проверьте год создания произведения (не может быть больше текущего)."
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")


class UserEmailSerializer(serializers.Serializer):
    username = serializers.SlugField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Нельзя использовать данный username")
        return value


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Reviews
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')
        read_only_fields = ('title',)
    
    def validate_author(self, data):
        if Reviews.objects.filter(author=data).exists:
            raise exceptions.ValidationError(
                'Отзыв от такого пользователя уже существует'
            )
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comments
        fields = ('id', 'author', 'review', 'text', 'pub_date')
        read_only_fields = ('review',)


class JWTTokenSerializer(serializers.Serializer):
    username = serializers.SlugField(required=True)
    confirmation_code = serializers.SlugField(required=True)
