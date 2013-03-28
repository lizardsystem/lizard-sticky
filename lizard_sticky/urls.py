from django.conf import settings
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin
from lizard_ui.urls import debugmode_urlpatterns

from views import StickyBrowserView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', StickyBrowserView.as_view(),
        name='lizard_sticky.sticky_browser'),
    url(r'^add_sticky/$',
        'lizard_sticky.views.add_sticky',
        name='lizard_sticky.add_sticky'),
    )
urlpatterns += debugmode_urlpatterns()

if getattr(settings, 'LIZARD_STICKY_STANDALONE', False):
    urlpatterns += patterns(
        '',
        (r'^map/', include('lizard_map.urls')),
        (r'^ui/', include('lizard_ui.urls')),
        (r'^admin/', include(admin.site.urls)),
    )
