# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from __future__ import print_function
from __future__ import unicode_literals
from django.contrib.gis import admin
from lizard_sticky.models import Sticky, Tag


class StickyAdmin(admin.GeoModelAdmin):
    list_display = ['title', 'reporter', 'tags_for_admin']
    search_fields = ['title', 'reporter', 'description',]
    list_filter = ('tags', )


admin.site.register(Sticky, StickyAdmin)
admin.site.register(Tag)
