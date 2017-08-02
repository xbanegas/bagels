# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .bookmarks.models import Bookmark
from .tags.models import Tag
from .serializers import BookmarkSerializer, TagSerializer
from .forms import BookmarkForm, QuickTagForm


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
    tag_form = QuickTagForm()
    context = {'nodes': tags, 'bookmark_list': bookmarks, 'form': form, 'tag_form': tag_form}
    return context


@login_required
def index(request):
    user_id = request.user.id
    template = 'bookmarks/bookmark_list.html'

    if request.method == 'GET':
        context = get_index_user_context(user_id)
        return render(request, template, context)

    if request.method == 'POST':
        request_POST = request.POST.copy()

        # Instantiate, Validate, Save New Tag Forms
        if 'name' in request_POST is not ['']: new_tag = True
        else: new_tag = None
        if new_tag:
            new_tag_form = QuickTagForm(request_POST)
            new_tag_form.instance.user = request.user
            if new_tag_form.is_valid():
                tg = new_tag_form.save(commit=True)
            else:
                new_tag = False
                tg = False
                print(new_tag_form.errors)

        # Validate Bookmark, Check for Duplicates, Optional Attach Tags, Save
        # And Return Appropriate Response
        form = BookmarkForm(request_POST)
        form.instance.user = request.user
        if form.is_valid():
            if not is_duplicate(form.cleaned_data['url'], user_id):
                bm = form.save(commit=True)
                if new_tag:
                    bm.tags.add(tg)
                context = get_index_user_context(user_id)
                return render(request, template, context)
            else:
                context = get_index_user_context(user_id)
                context['messages'] = ['duplicate link not saved']
                return render(request, template, context, status=400)
        else:
            print(form.errors)
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
        context = {'nodes': {}, 'bookmark_list': bookmarks, 'tag': {'name': tag_exists[0].name,'id': tag_id}}
        return render(request, template, context)
    # @TODO return proper response code
    else:
        return redirect('/')
