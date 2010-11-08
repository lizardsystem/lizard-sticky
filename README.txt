lizard-sticky
==========================================

Introduction


Requirements
------------

Make sure you have a geo enabled database. A good example is
postGIS. This app will NOT work on sqlite.


Usage
-----

- Add lizard_sticky to your buildout.cfg.

- Add 'lizard_sticky' and 'lizard_map' to the INSTALLED_APPS in your
  settings.

- Include lizard-sticky in your urls.py.
    (r'^sticky/', include('lizard_sticky.urls')),

- Refer to the sticky browser from somewhere:

{% url lizard_sticky.sticky_browser %}

or

reverse('lizard_sticky.sticky_browser')

- Run syncdb to make appropriate database tables.


Development installation
------------------------

The first time, you'll have to run the "bootstrap" script to set up setuptools
and buildout::

    $> python bootstrap.py

And then run buildout to set everything up::

    $> bin/buildout

(On windows it is called ``bin\buildout.exe``).

You'll have to re-run buildout when you or someone else made a change in
``setup.py`` or ``buildout.cfg``.

The current package is installed as a "development package", so
changes in .py files are automatically available (just like with ``python
setup.py develop``).

If you want to use trunk checkouts of other packages (instead of released
versions), add them as an "svn external" in the ``local_checkouts/`` directory
and add them to the ``develop =`` list in buildout.cfg.

Tests can always be run with ``bin/test`` or ``bin\test.exe``.
