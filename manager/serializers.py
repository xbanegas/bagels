from rest_framework import serializers

from .models import Bookmark, Tag

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        field = ('id', 'user', 'created', 'modified', 'url', 'title'
                'tags', 'notes')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        field = ('id', 'name')
