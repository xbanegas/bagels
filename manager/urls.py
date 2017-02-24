# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.shortcuts import render

from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
]
