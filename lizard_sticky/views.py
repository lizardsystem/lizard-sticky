from django.shortcuts import render_to_response
from django.template import RequestContext

from lizard_map.daterange import current_start_end_dates
from lizard_map.daterange import DateRangeForm
from lizard_map.workspace import WorkspaceManager
from lizard_sticky.models import Tag

def sticky_browser(request):
    """Show sticky browser.

    Automatically makes new workspace if not yet available

    """
    workspace_manager = WorkspaceManager(request)
    workspaces = workspace_manager.load_or_create()
    date_range_form = DateRangeForm(
        current_start_end_dates(request, for_form=True))
    return render_to_response(
        'lizard_sticky/sticky-browser.html',
        {'date_range_form': date_range_form,
         'workspaces': workspaces,
         'javascript_click_handler': 'sticky_popup_click_handler',
         'tags': Tag.objects.all(),
         },
        context_instance=RequestContext(request))
