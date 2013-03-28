# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from __future__ import print_function
from __future__ import unicode_literals
from django.contrib.gis import admin
from lizard_sticky.models import Sticky, Tag


admin.site.register(Sticky, admin.GeoModelAdmin)
admin.site.register(Tag)
