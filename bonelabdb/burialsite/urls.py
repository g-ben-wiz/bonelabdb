from django.conf.urls.defaults import *

urlpatterns = patterns('burialsite.views',
    (r'^$', 'homepage'),
    (r'^(?P<burial_site_id>\d+)/$', 'burial_site'),
    (r'^feature/(?P<burial_site_id>\d+)/(?P<feature_id>\d+)/$', 'feature'),
    (r'^skeleton/(?P<burial_site_id>\d+)/(?P<feature_id>\d+)/(?P<skeleton_id>\w+)/$', 'skeleton')
)

