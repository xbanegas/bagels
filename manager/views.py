# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.http import HttpResponse

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .bookmarks.models import Bookmark
from .tags.models import Tag
from .serializers import BookmarkSerializer, TagSerializer


# @TODO Move the api views to its own module
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


# @TODO Move to its own file or admin
class BookmarkForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ['title', 'url', 'tags', 'notes']


# @ TODO Move to utils, form, or Bookmark
def is_duplicate(url, user_id):
    queryset = Bookmark.objects.filter(user__id=user_id, url=url)
    return False if len(queryset) == 0 else True

# @ TODO Move to utils or form
def get_index_user_context(user_id):
    tags = Tag.objects.filter(user__id=user_id)
    bookmarks = Bookmark.objects.filter(user__id=user_id).order_by('-created')
    form = BookmarkForm()
    form.fields['tags'].queryset = tags
    context = {'nodes': tags, 'bookmark_list': bookmarks, 'form': form}
    return context


@login_required
def index(request):
    user_id = request.user.id
    template = 'bookmarks/bookmark_list.html'

    if request.method == 'GET':
        context = get_index_user_context(user_id)
        return render(request, template, context)

    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        form.instance.user = request.user

        if form.is_valid():
            if not is_duplicate(form.cleaned_data['url'], user_id):
                bm = form.save(commit=True)
                context = get_index_user_context(user_id)
                return render(request, template, context)
            else:
                context = get_index_user_context(user_id)
                context['messages'] = ['duplicate link not saved']
                return render(request, template, context, status=400)
        else:
            context = get_index_user_context(user_id)
            context['messages'] = ['invalid form data']
            return render(request, template, context, status=400)

# @TODO Make CBV
@login_required
def detail(request):
    pass

@login_required
def list_by_tag(request, tag_id):
    user_id = request.user.id
    template = 'bookmarks/bookmark_list_bytag.html'
    tag_exists = Tag.objects.filter(pk=tag_id)
    if request.method == 'GET' and tag_exists:
        bookmarks = Bookmark.objects.filter(user__id=user_id, tags__id=tag_id).order_by('-created')
        context = {'nodes': {}, 'bookmark_list': bookmarks}
        return render(request, template, context)
    # @TODO return proper response code
    else:
        return redirect('/')
