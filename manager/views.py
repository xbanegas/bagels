# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Bookmark, Tag
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
    return render(request, 'pages/home.html')
