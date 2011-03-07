import datetime

from django.contrib.auth.models import User
from django.contrib.gis.db import models


class Tag(models.Model):
    class Meta:
        ordering = ['slug']

    slug = models.SlugField()

    def __unicode__(self):
        return u'%s' % self.slug


class Sticky(models.Model):
    """
    Sticky
    """

    owner = models.ForeignKey(User, blank=True, null=True)
    datetime = models.DateTimeField(default=datetime.datetime.now())
    reporter = models.CharField(max_length=80)
    title = models.CharField(max_length=80)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    attachment = models.ImageField(upload_to='lizard-sticky',
                                   blank=True,
                                   null=True)

    # geo stuff
    geom = models.PointField()  # default srid 4326
    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s' % self.title

    def add_tags(self, slugs):
        """add tags to sticky

        tags is a list of strings
        """
        for slug in slugs:
            if slug:
                tag, _ = Tag.objects.get_or_create(slug=slug.lower())
                self.tags.add(tag)
