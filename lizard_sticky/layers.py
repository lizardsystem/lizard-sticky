"""
Adapter for lizard-sticky
"""
import os
import mapnik

from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.shortcuts import get_object_or_404

from lizard_map import adapter
from lizard_map import coordinates
from lizard_map import workspace
from lizard_map.coordinates import wgs84_to_google
from lizard_map.models import ICON_ORIGINALS
from lizard_map.symbol_manager import SymbolManager
from lizard_sticky.models import Sticky

ICON_STYLE = {'icon': 'sticky.png',
              'mask': ('sticky_mask.png', ),
              'color': (1, 1, 0, 0)}

class WorkspaceItemAdapterSticky(workspace.WorkspaceItemAdapter):
    def __init__(self, *args, **kwargs):
        """
        tags: list or queryset of tags

        If no tags are selected, all stickies are selected!
        """
        super(WorkspaceItemAdapterSticky, self).__init__(*args, **kwargs)
        self.tags = []
        if 'tags' in self.layer_arguments:
            self.tags = self.layer_arguments['tags']

    def style(self):
        """
        Make mapnik point style
        """
        symbol_manager = SymbolManager(
            ICON_ORIGINALS,
            os.path.join(settings.MEDIA_ROOT, 'generated_icons'))
        output_filename = symbol_manager.get_symbol_transformed(
            ICON_STYLE['icon'], **ICON_STYLE)
        output_filename_abs = os.path.join(
            settings.MEDIA_ROOT, 'generated_icons', output_filename)
        # use filename in mapnik pointsymbolizer
        point_looks = mapnik.PointSymbolizer(output_filename_abs, 'png', 16, 16)
        point_looks.allow_overlap = True
        layout_rule = mapnik.Rule()
        layout_rule.symbols.append(point_looks)
        point_style = mapnik.Style()
        point_style.rules.append(layout_rule)

        return point_style
        
    def layer(self, layer_ids=None):
        """Return a layer with all stickies or stickies with selected
        tags
        """
        layers = []
        styles = {}
        layer = mapnik.Layer("Stickies", coordinates.WGS84)
        layer.srs = coordinates.WGS84

        if settings.DATABASE_ENGINE:
            # old database settings
            db_settings = {}
            db_settings['HOST'] = settings.DATABASE_HOST
            db_settings['USER'] = settings.DATABASE_USER
            db_settings['PASSWORD'] = settings.DATABASE_PASSWORD
            db_settings['NAME'] = settings.DATABASE_NAME
            db_settings['ENGINE'] = settings.DATABASE_ENGINE
        else:
            # new database settings
            db_settings = settings.DATABASES['default']

        if db_settings['ENGINE'] == 'sqlite3' or \
                db_settings['ENGINE'] == 'django.contrib.gis.db.backends.spatialite':
            datasource = mapnik.SQLite
            options = {'file': settings.DATABASES['default']['NAME']}
            query = (
                'select geom from lizard_sticky_sticky')
        elif db_settings == 'postgresql_psycopg2' or \
                db_settings['ENGINE'] == 'django.contrib.gis.db.backends.postgis':
            datasource = mapnik.PostGIS
            options = {'host': db_settings['HOST'],
                       'user': db_settings['USER'],
                       'password': db_settings['PASSWORD'],
                       'dbname': db_settings['NAME']}
            if self.tags:
                # make an inner join with given tags
                query = (
                    '(select sticky.geom from '
                    '  lizard_sticky_sticky as sticky, lizard_sticky_tag as tag, '
                    '  lizard_sticky_sticky_tags as sticky_tags '
                    'where '
                    '  sticky_tags.sticky_id = sticky.id and '
                    '  sticky_tags.tag_id = tag.id and '
                    '  (%s) '
                    ') lizard_sticky_sticky' % \
                    ' or '.join(['tag.slug = \'%s\'' % tag for tag in self.tags])
                    )
            else:
                query = (
                    '(select geom from lizard_sticky_sticky) lizard_sticky_sticky')
            # ^^^ Note: only works properly with postgresql, apparently.
        else:
            raise RuntimeError(
                'Sorry, unconfigured db engine (%s%s) for mapnik integration.' % (
                    db_settings['ENGINE']))

        options['geometry_field'] = 'geom'

        layer.datasource = datasource(table=str(query), **options)

        # generate "unique" point style name and append to layer
        style_name = "Stickies %r " % self.tags
        styles[style_name] = self.style()
        layer.styles.append(style_name)

        layers = [layer, ]
        return layers, styles

    def search(self, google_x, google_y, radius=None):
        """
        returns a list of dicts with keys distance, name, shortname,
        google_coords, workspace_item, identifier
        """
        # wgs84_x, wgs84_y = google_to_wgs84(google_x, google_y)
        pnt = Point(google_x, google_y, srid=900913)
        stickies = Sticky.objects.filter(geom__distance_lte=(pnt, D(m=radius*0.5)))

        result = [{'distance': 0.0,
                   'name': '%s (%s)' % (sticky.title, sticky.reporter),
                   'shortname': str(sticky.title),
                   'template': 'lizard_sticky/popup_sticky.html',
                   'object': sticky,
                   'google_coords': wgs84_to_google(sticky.geom.x, sticky.geom.y),
                   'workspace_item': self.workspace_item,
                   'identifier': {'sticky_id': sticky.id},
                   } for sticky in stickies]
        return result

    def location(self, sticky_id):
        sticky = get_object_or_404(Sticky, pk=sticky_id)
        return {
            'name': '%s (%s)' % (sticky.title, sticky.reporter),
            'shortname': str(sticky.title),
            'workspace_item': self.workspace_item,
            'identifier': {'sticky_id': sticky.id},
            'google_coords': wgs84_to_google(sticky.geom.x, sticky.geom.y),
            'template': 'lizard_sticky/popup_sticky.html',
            'object': sticky,
            }

    def symbol_url(self, identifier=None, start_date=None, end_date=None):
        return super(WorkspaceItemAdapterSticky, self).symbol_url(
            identifier=identifier,
            start_date=start_date,
            end_date=end_date,
            icon_style=ICON_STYLE)
