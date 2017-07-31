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
        regex=r"^api/bookmarks/$",
        view=views.BookmarkCreateReadView.as_view(),
        name="link_rest_api"
    ),
    url(
        regex=r"^api/bookmarks/(?P<id>[0-9]+)/$",
        view=views.BookmarkReadUpdateDeleteView.as_view(),
        name="link_rest_api_detail"
    ),
    url(
        regex=r"^api/tags/$",
        view=views.TagCreateReadView.as_view(),
        name="tag_rest_api"
    ),
    url(
        regex=r"^api/tags/(?P<id>[0-9]+)/$",
        view=views.TagReadUpdateDeleteView.as_view(),
        name="tag_rest_api_detail"
    )
]
