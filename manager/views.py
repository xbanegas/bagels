# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.contrib import messages

from .bookmarks.models import Bookmark
from .tags.models import Tag
from .forms import BookmarkForm, QuickTagForm


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


def get_detail_user_context(user_id, bookmark):
    tags = Tag.objects.filter(user__id=user_id)
    form = BookmarkForm(initial=model_to_dict(bookmark))
    tag_form = QuickTagForm()
    context = {'nodes': tags, 'form': form, 'tag_form': tag_form, 'bookmark': bookmark}
    return context


def save_form_and_response(request, request_POST, template, bookmark, edit=False):
    user_id = request.user.id

    # Instantiate, Validate, Save New Tag Forms
    if request_POST['name']:
        new_tag_form = QuickTagForm(request_POST)
        new_tag_form.instance.user = request.user
        if new_tag_form.is_valid():
            new_tag = new_tag_form.save(commit=True)
        else:
            print(new_tag_form.errors)
    else:
        new_tag = False

    # Validate Bookmark, Check for Duplicates, Optional Attach Tags, Save
    # And Return Appropriate Response
    form = BookmarkForm(request_POST, instance=bookmark)
    form.instance.user = request.user
    if form.is_valid():
        if edit or not is_duplicate(form.cleaned_data['url'], user_id):
            bm = form.save(commit=True)
            if new_tag:
                bm.tags.add(new_tag)
            if edit:
                context = get_detail_user_context(user_id, bookmark)
                messages.success(request, 'Bookmark Saved')
            else:
                context = get_index_user_context(user_id)
            return render(request, template, context)
        else:
            context = get_index_user_context(user_id)
            messages.warning(request, 'Duplicate link not saved')
            return render(request, template, context, status=400)
    else:
        print(form.errors)
        context = get_index_user_context(user_id)
        messages.error(request, 'Check the form and try again')
        return render(request, template, context, status=400)


@login_required
def index(request):
    user_id = request.user.id
    template = 'bookmarks/home.html'

    if request.method == 'GET':
        context = get_index_user_context(user_id)
        return render(request, template, context)

    if request.method == 'POST':
        request_POST = request.POST.copy()
        return save_form_and_response(request, request_POST, template, bookmark=None, edit=False)


@login_required
def bookmark_detail(request, bookmark_id):
    user_id = request.user.id
    template = 'bookmarks/detail.html'
    bookmark = get_object_or_404(Bookmark, pk=bookmark_id)

    if request.method == 'GET':
        context = get_detail_user_context(user_id=user_id, bookmark=bookmark)
        return render(request, template, context)

    if request.method == 'POST':
        request_POST = request.POST.copy()
        return save_form_and_response(request, request_POST, template, bookmark, edit=True)


@login_required
def bookmark_delete(request, bookmark_id):
    template = 'bookmarks/delete.html'
    bookmark = get_object_or_404(Bookmark, pk=bookmark_id)

    if request.method == 'GET':
        context = {'bookmark': bookmark}
        return render(request, template, context)

    if request.method == 'POST':
        bookmark.delete()
        return redirect('manager:home', permanent=True)


@login_required
def list_by_tag(request, tag_id):
    user_id = request.user.id
    template = 'bookmarks/list_by_tag.html'
    tag = get_object_or_404(Tag, pk=tag_id)

    if request.method == 'GET':
        bookmarks = Bookmark.objects.filter(user__id=user_id, tags__id=tag_id).order_by('-created')
        context = {'nodes': {}, 'bookmark_list': bookmarks, 'tag': tag}
        return render(request, template, context)
