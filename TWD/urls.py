from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from burger import views
from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return '/burger/'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TWD.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^burger/', include('burger.urls')),
    # no activation email would be sent
    (r'^accounts/', include('registration.backends.simple.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )