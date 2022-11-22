from rest_framework import filters, mixins, viewsets
from rest_framework.viewsets import GenericViewSet, viewsets

from .models import Categories, Genres, Titles, Rewiews


class RewiewsViewSet(viewsets.ModelViewSet,):
    queryset = Rewiews.objects.all()
    