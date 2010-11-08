from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',
        'lizard_sticky.views.sticky_browser',
        name='lizard_sticky.sticky_browser'),
    url(r'^add_sticky/$',
        'lizard_sticky.views.add_sticky',
        name='lizard_sticky.add_sticky'),
    (r'^map/', include('lizard_map.urls')),
    )


if settings.DEBUG:
    # Add this also to the projects that use this application
    urlpatterns += patterns(
        '',
        (r'', include('staticfiles.urls')),
        (r'^admin/', include(admin.site.urls)),
    )
