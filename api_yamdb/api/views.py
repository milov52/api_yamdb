from rest_framework import filters, viewsets

from api.serializers import CategoriesSerializer, GenresSerializer, TitlesSerializer
from reviews.models import Categories, Genres, Titles


class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenresViewSet(viewsets.ModelViewSet):
    serializer_class = GenresSerializer
    queryset = Genres.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitlesViewSet(viewsets.ModelViewSet):
    serializer_class = TitlesSerializer
    queryset = Titles.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("category", "genre", "name", "year")
