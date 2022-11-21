from rest_framework import filters, mixins, viewsets
from rest_framework.viewsets import GenericViewSet

from api.serializers import CategoriesSerializer, GenresSerializer, TitlesSerializer
from reviews.models import Categories, Genres, Titles


class CategoriesViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = CategoriesSerializer
    queryset = Categories.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = 'slug'


class GenresViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = GenresSerializer
    queryset = Genres.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    serializer_class = TitlesSerializer
    queryset = Titles.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ("category", "genre", "name", "year")
