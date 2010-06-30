"""
Adapter for lizard-sticky
"""
import mapnik

from lizard_map import adapter
from lizard_map import coordinates


class WorkspaceItemAdapterSticky(workspace.WorkspaceItemAdapter):
    def __init__(self, selected_tags=None, *args, **kwargs):
        """
        Selected_tags: list or queryset of tags

        If no tags are selected, all stickies are selected!
        """
        super(WorkspaceItemAdapterSticky, self).__init__(*args, **kwargs)
        self.tags = []
        if selected_tags:
            self.tags = selected_tags

    def style(self):
        """
        Make mapnik point style
        """
        symbol_manager = SymbolManager(
            ICON_ORIGINALS,
            os.path.join(settings.MEDIA_ROOT, 'generated_icons'))
        icon_style = {'icon': 'meetpuntPeil.png',
                      'mask': ('meetpuntPeil_mask.png', ),
                      'color': (1, 1, 0, 0)}
        output_filename = symbol_manager.get_symbol_transformed(
            icon_style['icon'], **icon_style)
        output_filename_abs = os.path.join(
            settings.MEDIA_ROOT, 'generated_icons', output_filename)
        # use filename in mapnik pointsymbolizer
        point_looks = mapnik.PointSymbolizer(output_filename_abs, 'png', 32, 32)
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
        layer = mapnik.Layer("Stickies", coordinates.RD)

        layer.datasource = mapnik.PointDatasource()
        if self.tags:
            stickies = Sticky.objects.all()
        else:
            stickies = Sticky.objects.filter(tag__in=self.tags)
        for sticky in stickies:
            x, y = coordinates.google_to_rd(sticky.google_x, sticky.google_y)
            layer.datasource.add_point(
                x, y, 'Name', sticky.title)

        # generate "unique" point style name and append to layer
        style_name = "Stickies %r " % self.tags
        styles[style_name] = self.style()
        layer.styles.append(style_name)

        layers = [layer, ]
        return layers, styles
        
