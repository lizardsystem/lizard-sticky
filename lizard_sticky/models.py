from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Tag(models.Model):
    slug = models.SlugField()

    def __unicode__(self):
        return u'%s' % self.slug

class Sticky(models.Model):
    """
    Sticky
    """

    owner = models.ForeignKey(User, blank=True, null=True)
    reporter = models.CharField(max_length=80)
    title = models.CharField(max_length=80)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    attachment = models.ImageField(upload_to='lizard-sticky', blank=True, null=True)

    # geo stuff
    # google_x = models.FloatField()
    # google_y = models.FloatField()
    geom = models.PointField()  # srid 4326
    objects = models.GeoManager()

    def __unicode__(self):
        return u'%s' % self.title
    
