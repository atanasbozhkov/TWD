from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from burger import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TWD.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^KC/', include('KC.urls')),
    url(r'^burger/', include('burger.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )