from rest_framework import serializers

from reviews.models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'

class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer()
    genre = GenresSerializer(many=True)
    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')