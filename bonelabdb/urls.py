from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'burialsite.views.home_redirect'),
    (r'^logout/$', 'burialsite.views.sitelogout'),
    (r'^login/$', 'burialsite.views.sitelogin'),
    (r'^invalidlogin/$', 'burialsite.views.invalidlogin'),
    (r'^invalidlogin/$', 'burialsite.views.disabledaccount'),
    (r'^burialsite/', include('burialsite.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

