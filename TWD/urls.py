from django.conf.urls import patterns, include, url
from django.contrib import admin
from TWD import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^burger/', include('burger.urls'))
)

