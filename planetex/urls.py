from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^$', 'planetex.apps.planetex.views.index'),
    (r'^atom/$', 'planetex.apps.planetex.views.atom'),
    (r'^cloud/$', 'planetex.apps.planetex.views.wordcloud'),
    (r'^opml/$', 'planetex.apps.planetex.views.opml'),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls.admin')),
    (r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root' : '/home/rvr/django/planetex/static/', 'show_indexes':True}),
)
