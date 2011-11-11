from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from lizard_map.views import AppView

from lizard_map import coordinates
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
    x,y (google)
    tags -> split into separated tags
    """
    reporter = request.POST.get("reporter")
    title = request.POST.get("title")
    description = request.POST.get("description")
    x = request.POST.get("x")
    y = request.POST.get("y")
    geom = Point(float(x), float(y))
#    TODO: Jack deleted coordinates.MapSettings -- check
#          if it's not still needed for this.
#    map_settings = coordinates.MapSettings()

    tags = request.POST.get("tags", "")

    sticky = Sticky(reporter='reporter',
                    title='title',
                    description='description',
                    geom=Point(0.0, 0.0))

    sticky.save()

    sticky.add_tags(tags.split(" "))
    return HttpResponse("")
