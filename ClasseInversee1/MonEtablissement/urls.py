# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from MonEtablissement import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login),
    url(r'^(?P<etablissement_text>.+)/sequence/(?P<niveau_int>\d+)eme/$', views.sequence, name='sequence'),
    url(r'welcome$', views.welcome, name='welcome')
    
)