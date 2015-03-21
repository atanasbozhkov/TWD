from django.conf.urls import patterns, include, url
from django.contrib import admin
from TWD import views
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^burger/', include('burger.urls')),
    url(r'^admin/', include(admin.site.urls)),

)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )