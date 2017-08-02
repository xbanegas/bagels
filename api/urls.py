# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(
        regex=r"^bookmarks/$",
        view=views.BookmarkCreateReadView.as_view(),
        name="link_rest_api"
    ),
    url(
        regex=r"^bookmarks/(?P<id>[0-9]+)/$",
        view=views.BookmarkReadUpdateDeleteView.as_view(),
        name="link_rest_api_detail"
    ),
    url(
        regex=r"^tags/$",
        view=views.TagCreateReadView.as_view(),
        name="tag_rest_api"
    ),
    url(
        regex=r"^tags/(?P<id>[0-9]+)/$",
        view=views.TagReadUpdateDeleteView.as_view(),
        name="tag_rest_api_detail"
    )
]
