from rest_framework import serializers
from datetime import datetime
from reviews.models import Categories, GenreTitles, Genres, Titles


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
    description = serializers.StringRelatedField(required=False)

    class Meta:
        model = Titles
        fields = ("id", "name", "year", "rating", "description", "genre", "category")

    def validate_year(self, value):
        current_year = datetime.now().year
        if not 0 <= value <= current_year:
            raise serializers.ValidationError(
                'Проверьте год создания произведения (не может быть больше текущего).'
            )
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Titles.objects.create(**validated_data)
        for genre in genres:
            GenreTitles.objects.create(
                genre=genre, title=title
            )
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)

        genres_data = validated_data.pop('genre')
        instance.genre.set(genres_data)

        instance.save()
        return instance
