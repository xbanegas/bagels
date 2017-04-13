# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .bookmarks.models import Bookmark
from .tags.models import Tag
from .serializers import BookmarkSerializer, TagSerializer

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

@login_required
def index(request):
    user_id = request.user.id
    tags = Tag.objects.filter(user__id=user_id)
    bookmarks = Bookmark.objects.filter(user__id=user_id)
    context = {'tag_list': tags, 'bookmark_list': bookmarks}
    return render(request, "bookmarks/bookmark_list.html", context)
