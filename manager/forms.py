from django import forms
from django.forms import ModelForm

from .bookmarks.models import Bookmark
from .tags.models import Tag


class BookmarkForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ['title', 'url', 'tags', 'notes']
        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }


class QuickTagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
