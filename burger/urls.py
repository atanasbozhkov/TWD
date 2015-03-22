from django.conf.urls import patterns, url
from burger import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^categoryList/', views.categoryList, name='categoryList'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^add_page/(?P<category_name_slug>[\w\-]+)/$', views.add_page, name='add_page'),
    url(r'^add_place/', views.add_place, name='add_place'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
)