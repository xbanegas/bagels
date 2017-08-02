# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.index,
        name='home'
    ),
    url(
        regex=r"^list/(?P<tag_id>[0-9]+)/$",
        view=views.list_by_tag,
        name='list_by_tag'
    ),
    url(
        regex=r"^bookmark/(?P<bookmark_id>[0-9]+)/$",
        view=views.bookmark_detail,
        name='bookmark_detail'
    ),
]
