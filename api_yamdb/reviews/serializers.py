from rest_framework import serializers

from .models import Rewiews, Comments

class RewiewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Rewiews
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')
        read_only_fields = ('title',)

class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comments
        fields = ('id', 'author', 'rewiew', 'text', 'pub_date')
        read_only_fields = ('rewiew',)