from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from lizard_map.coordinates import google_to_wgs84
from lizard_map.daterange import current_start_end_dates
from lizard_map.daterange import DateRangeForm
from lizard_map.workspace import WorkspaceManager
from lizard_sticky.models import Sticky
from lizard_sticky.models import Tag


def sticky_browser(request,
                   template='lizard_sticky/sticky-browser.html',
                   crumbs_prepend=None):
    """Show sticky browser.

    Automatically makes new workspace if not yet available

    """
    workspace_manager = WorkspaceManager(request)
    workspaces = workspace_manager.load_or_create()
    date_range_form = DateRangeForm(
        current_start_end_dates(request, for_form=True))

    if crumbs_prepend is not None:
        crumbs = list(crumbs_prepend)
    else:
        crumbs = [{'name': 'home', 'url': '/'}]
    crumbs.append({'name': 'meldingen',
                   'url': reverse('lizard_sticky.sticky_browser')})

    return render_to_response(
        template,
        {'date_range_form': date_range_form,
         'workspaces': workspaces,
         'javascript_hover_handler': 'popup_hover_handler',
         'javascript_click_handler': 'sticky_popup_click_handler',
         'tags': Tag.objects.all(),
         'crumbs': crumbs,
         },
        context_instance=RequestContext(request))


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
    wgs84_x, wgs84_y = google_to_wgs84(float(x), float(y))
    geom = Point(wgs84_x, wgs84_y)
    tags = request.POST.get("tags", "")

    sticky = Sticky(reporter=reporter,
                    title=title,
                    description=description,
                    geom=geom)
    sticky.save()
    sticky.add_tags(tags.split(" "))
    return HttpResponse("")
