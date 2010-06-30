from lizard_map.daterange import DateRangeFrom
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
        'lizard_map/sticky-browser.html',
        {'date_range_form': date_range_form,
         'workspaces': workspaces,
         'javascript_click_handler': 'popup_click_handler',
         'tags': Tag.objects.all(),
         },
        context_instance=RequestContext(request))


