from django.contrib import admin

from .bookmarks.models import Bookmark
from .tags.models import Tag

admin.site.register(Bookmark)
admin.site.register(Tag)
