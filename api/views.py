from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .serializers import BookmarkSerializer, TagSerializer

from manager.bookmarks.models import Bookmark
from manager.tags.models import Tag


class BookmarkQueryMixin(object):
    def get_queryset(self):
        user = self.request.user.id
        return Bookmark.objects.filter(user__id=user)


class TagQueryMixin(object):
    def get_queryset(self):
        user = self.request.user.id
        return Tag.objects.filter(user__id=user)


class BookmarkCreateReadView(BookmarkQueryMixin, ListCreateAPIView):
    serializer_class = BookmarkSerializer
    lookup_field = 'id'


class BookmarkReadUpdateDeleteView(BookmarkQueryMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = BookmarkSerializer
    lookup_field = 'id'


class TagCreateReadView(TagQueryMixin, ListCreateAPIView):
    serializer_class = TagSerializer
    lookup_field = 'id'


class TagReadUpdateDeleteView(TagQueryMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    lookup_field = 'id'

