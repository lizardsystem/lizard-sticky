Changelog of lizard-sticky
===================================================


2.2 (unreleased)
----------------

- Nothing changed yet.


2.1 (2013-03-29)
----------------

- Beautified the admin interface: showing more columns in the list interface
  and allowing filtering on tag.


2.0 (2013-03-28)
----------------

- Moved to github: https://github.com/lizardsystem/lizard-sticky.

- **Upgrade warning**: south migrations added. For existing sites, you'll need
  a ``bin/django migrate --fake lizard_sticky 0001``.


1.13 (2012-12-19)
-----------------

- Fixed urls.py, so it won't recusively include other lizard-* URLs when
  running as part of a site.


1.12 (2012-12-17)
-----------------

- Minor tree styling.


1.11 (2012-11-27)
-----------------

- Convert to Lizard 4.0.

- Add support for the legend.

- Properly set dependency versions.


1.10 (2011-12-20)
-----------------

- Fixed add to collage button in popup.

- Made saving work again.

- Require latest lizard-map (3.8).


1.9 (2011-11-11)
----------------

- Modernized buildout.cfg somewhat

- Changed views to classes to work with latest lizard-map. Updated
  templates to reflect this.

- Changed setup.py to require at least the currently latest
  lizard-map (3.4.2) and lizard-ui (3.7).

- Added dependency of map >= 1.60.


1.8 (2011-04-21)
----------------

- Removed unnecessary workspace_manager and date_range_form stuff. It
  is also incompatible with map >= 1.71.


1.7.2 (2011-04-14)
------------------

- Removed popup header (looks better).


1.7.1 (2011-03-01)
------------------

- Removed print statement.


1.7 (2011-03-01)
----------------

- Fixed sticky coordinate storage.


1.6 (2011-02-28)
----------------

- Changed storage for x, y coordinates: Coordinates are
  now saved in original projection (i.e. google, rd). When drawing
  layer, tell mapnik the projection setting in MAP_SETTINGS. This also
  fixes a problem when the client is not in 900913
  projection. Requires lizard-map 1.55 or higher.


1.5 (2011-02-15)
----------------

- Moved sticky.png to app_icons subdir.


1.4 (2011-02-03)
----------------

- Fixed breadcrumbs bug.


1.3 (2011-02-01)
----------------

- Minor layout changes.

- Added option crumbs_prepend (see lizard_ui).


1.2 (2010-12-10)
----------------

- Renamed "Geeltje" to "Melding".


1.1 (2010-11-08)
----------------

- Updated readme.

- Added sticky icon.

- Bugfix draw multiple stickies close to each other to compensate #402.


1.0 (2010-09-22)
----------------

- Bugfix posting stickies.

- Clean up some code.


0.8 (2010-09-22)
----------------

- Bugfix: add preventDefault to js. This will prevent the js to reload
  the page after posting a new sticky.


0.7 (2010-09-22)
----------------

- Bugfix: "show all stickies" was broken.

- Bugfix: better compensation for mapnik bug #402.


0.6 (2010-09-22)
----------------

- Bugfix: prevent javascript to reload page (by adding "return
  false").

- Bugfix: layers that filters tags now work.

- Bugfix: do not add "empty" tags.


0.5 (2010-09-03)
----------------

- Removed mapnik custom database query stuff, replaced by standard
  django requests and building points layer manually.


0.4 (2010-09-01)
----------------

- Fixed stickies by searching just by ID instead of by elementtype#id
  combinations.  The bug was that one of the elements changed type recently.


0.3 (2010-08-30)
----------------

- Refactor add-sticky to new popup style.


0.2 (2010-08-18)
----------------

- Adjusted to lizard-map's adapter changes and snippet group functionality.


0.1 (2010-07-15)
----------------

- Tags can be used as filters on sticky layer.
- Navigate through stickies and put new stickies using the map.
- Initial library skeleton created by nensskel.  [Jack]
