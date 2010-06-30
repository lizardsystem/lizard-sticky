from django.db import models

class Tag(models.Model):
    slug = models.SlugField()

    def __unicode__(self):
        return u'%s' % self.slug

class Sticky(models.Model):
    """
    Sticky
    """

    owner = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=80)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    description = models.TextField()
    attachment = models.ImageField(upload_to='sticky', blank=True, null=True)

    # geo stuff
    google_x = models.FloatField()
    google_y = models.FloatField()

    def __unicode__(self):
        return u'%s' % self.name
    
