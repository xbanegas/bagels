# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.forms.models import model_to_dict
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone

from .bookmarks.models import Bookmark
from .tags.models import Tag
from .forms import BookmarkForm, QuickTagForm, BookmarkImportFilesForm
from .utils.handle_import import handle


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
    context = {
        'nodes': tags,
        'bookmark_list': bookmarks,
        'form': form,
        'tag_form': tag_form
    }
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
    # Check for tag name or else no new tags to save
    if request_POST.get('name', False):
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
        if 'debug' in request.session:
            context['debug'] = request.session['debug']
        else:
            context['debug'] = None
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


@login_required
def bookmark_import(request):
    template = 'bookmarks/import.html'
    form = BookmarkImportFilesForm()
    context = {'form': form, 'data': {}}
    if request.method == 'GET':
        return render(request, template, context)
    if request.method == 'POST':
        form = BookmarkImportFilesForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            bm_list = {}
            bm_list = handle(files, bm_list)
            context['bm_list'] = bm_list
            request.session['confirm_list'] = bm_list
            return redirect(reverse('manager:bookmark_import_confirm'))


@login_required
def bookmark_import_confirm(request):
    template = 'bookmarks/import_confirm.html'
    context = {}
    confirm_list = request.session['confirm_list']

    if request.method == 'GET':
        # Create the Formset
        BookmarkFormSet = formset_factory(
            BookmarkForm,
            extra=confirm_list['count'] - 1
        )
        # discard count for zipping with form later
        confirm_list.pop('count', None)
        # Set time tag
        formset = BookmarkFormSet(initial=[
            # 1.11/ref/forms/api/#django.forms.Form.initial
            # @TODO check on tags
            {'tags': ['i{}'.format(timezone.now())]}
        ])
        # set url and source tag values in form to confirm
        links_list = []
        for source, links in confirm_list.items():
            for link in links:
                links_list.append({'source': source, 'url': link})
        for link, form in zip(links_list, formset):
            data = {'url':link['url'], 'title': link['source'] + '-import'}
            form.initial = data

        context['formset'] = formset
        return render(request, template, context)

    if request.method == 'POST':
        BookmarkFormSet = formset_factory(BookmarkForm)
        formset = BookmarkFormSet(request.POST)
        request.session['debug'] = []
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    request.session['debug'].append(
                        form.cleaned_data.get('url')
                    )

        # for data
        # context['debug'] = request.POST
        # return render(request, template, context)
        return redirect('manager:home', permanent=True)
