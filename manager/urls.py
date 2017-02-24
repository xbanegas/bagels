# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.shortcuts import render

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(
        regex=r"^api/links/$",
        view=views.BookmarkCreateReadView.as_view(),
        name="link_rest_api"
    ),
    url(
        regex=r"^api/links/(?P<id>[0-9]+)/$",
        view=views.BookmarkReadUpdateDeleteView.as_view(),
        name="link_rest_api"
    ),
    url(
        regex=r"^api/tags/$",
        view=views.TagCreateReadView.as_view(),
        name="tag_rest_api"
    ),
    url(
        regex=r"^api/tags/(?P<id>[0-9]+)/$",
        view=views.TagReadUpdateDeleteView.as_view(),
        name="tag_rest_api"
    )
]
