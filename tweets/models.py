from django.db import models

# Create your models here.


class Link(models.Model):
    """(Links description)"""
    
    url = models.URLField(blank=False, verify_exists=False)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"%s" % (self.link)

class Tweet(models.Model):
    """(Tweets description)"""
    raw_atom_entry = models.TextField(blank=True)
    tweet_link = models.URLField(blank=False, verify_exists=False,unique=True)
    raw = models.TextField(blank=False)
    created = models.DateTimeField(blank=True)
    found = models.DateTimeField(blank=False, auto_now_add=True)
    author = models.CharField(blank=True, max_length=250)
    links = models.ManyToManyField(Link,blank=True)
    
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"%s" % (self.raw)
