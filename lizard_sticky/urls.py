from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

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

if getattr(settings, 'LIZARD_STICKY_STANDALONE', False):
    urlpatterns += patterns(
        '',
        (r'^map/', include('lizard_map.urls')),
        (r'^admin/', include(admin.site.urls)),
        (r'', include('staticfiles.urls')),
    )
