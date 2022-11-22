from rest_framework import filters, mixins, viewsets, permissions
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet, viewsets

from .permissions import IsAuthorOrReadOnly, ReadOnly
from .serializers import RewiewsSerializer, CommentsSerializer
from .models import Titles, Rewiews


class RewiewsViewSet(viewsets.ModelViewSet):
    serializer_class = RewiewsSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    
    def get_permissions(self):
        if self.action ==' retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs['title_id'])
        return title.rewiews.all()

    def preform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs['title_id'])
        serializer.save(title=title, author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permissions_classes = (IsAuthorOrReadOnly)
    
    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()
    
    def get_queryset(self):
        rewiew = get_object_or_404(Rewiews, id=self.kwargs['rewiew_id'])
        return rewiew.comments.all()
    
    def preform_create(self, serializer):
        rewiew = get_object_or_404(Rewiews, id=self.kwargs['rewiew_id'])
        serializer.save(rewiew=rewiew, author=self.request.user)