from rest_framework import serializers

from manager.bookmarks.models import Bookmark
from manager.tags.models import Tag

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ('id', 'user', 'created', 'modified', 'url', 'title',
                'tags', 'notes')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'parent', 'created', 'modified')
