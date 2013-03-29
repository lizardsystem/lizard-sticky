# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from __future__ import print_function
from __future__ import unicode_literals

from django.http import HttpResponse
from lizard_map import coordinates
from lizard_map.views import AppView

from lizard_sticky.models import Sticky
from lizard_sticky.models import Tag


class StickyBrowserView(AppView):
    """Show sticky browser.

    Automatically makes new workspace if not yet available

    """

    template_name = 'lizard_sticky/sticky-browser.html'
    javascript_hover_handler = 'popup_hover_handler'
    javascript_click_handler = 'sticky_popup_click_handler'

    def tags(self):
        return Tag.objects.all()


def add_sticky(request):
    """
    add new sticky.

    req. from POST:
    reporter
    title
    description
    x,y (project is configured in the site's Settings)
    tags -> split into separated tags
    """
    reporter = request.POST.get("reporter")
    title = request.POST.get("title")
    description = request.POST.get("description")
    x = request.POST.get("x")
    y = request.POST.get("y")

    # Transform from the site's configured projection to wgs84
    geom = coordinates.transform_point(float(x), float(y), to_proj='wgs84')

    tags = request.POST.get("tags", "")

    sticky = Sticky(reporter=reporter,
                    title=title,
                    description=description,
                    geom=geom)

    sticky.save()

    sticky.add_tags(tags.split(" "))
    return HttpResponse("")
