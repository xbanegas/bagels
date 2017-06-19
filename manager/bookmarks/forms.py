from django import forms
from django.forms import ModelForm

from .models import Bookmark


class BookmarkCreateForm(ModelForm):

    class Meta:
        model = Bookmark
        fields = ('url', 'title', 'tags', 'notes')
        error_messages = {
            'url': {'duplicate_link' : 'This url already exists.'}
        }


    def clean_url(self):
        url = self.cleaned_data['url']
        qset = Bookmark.objects.filter(user__id=user_id, url=url)
        if len(qset) == 0:
            return url
        else:
            raise forms.ValidationError(self.error_messages['duplicate_link'])
