from django.conf.urls import patterns, url
from django.conf import settings
from burger import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add_place/', views.add_restaurant, name='add_place'),
    url(r'^newburger/', views.add_burger, name='add_burger'),
    url(r'^register/$', views.register, name='register'),
    url(r'^nearby/$', views.map_view, name='map_view'),
    url(r'^add_burger_category/$', views.add_burger_category, name='add_burger_category'),
    url(r'^burgersurfing/$', views.browse_burger, name='browse_burger'),
    url(r'^(?P<burger_slug>[\w\-]+)/$', views.burger_page, name='burger_page'),
    url(r'^getPicture', views.getPictures, name='get_burger_picture'),
)

if settings.REGISTRATION_OPEN:
    urlpatterns += patterns('', url(r'^register/$', views.register, name='register'))
else:
    urlpatterns += patterns('', url(r'^register/$', views.registerClosed, name='register'))
