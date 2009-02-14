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
        
        
class TweetManager(models.Manager):

    def top_tweets(self):
        import re
        
        songs = {}
        tweets = self.all().order_by("created")
        # Re's
        songly   = re.compile("http://song.ly/\w{1,5}",re.IGNORECASE)
        tinysong = re.compile("http://tinysong.com/\w{1,5}",re.IGNORECASE)
        twisten  = re.compile("http://twisten.fm/l/\w{1,5}",re.IGNORECASE)
        twiturm  = re.compile("http://twiturm.com/\w{1,5}",re.IGNORECASE)
        trakz    = re.compile("http://tra.kz/\w{1,5}",re.IGNORECASE)
        
        patterns = [songly, tinysong, twisten, twiturm,trakz]
        for tweet in tweets:
            #print tweet.raw
            for pattern in patterns:
                matches = pattern.findall(tweet.raw)
                if len(matches) > 0:
                    print matches[0]
                    if songs.get(matches[0],None):
                        songs[matches[0]] += 1
                    else:
                        songs[matches[0]] = 1
                    break
                    
                    
        alist = sorted(songs.iteritems(), key=lambda (k,v): (v,k) ,reverse=True)
        
        return alist[0:10]


class Tweet(models.Model):
    """(Tweets description)"""
    raw_atom_entry = models.TextField(blank=True)
    tweet_link = models.URLField(blank=False, verify_exists=False,unique=True)
    raw = models.TextField(blank=False)
    created = models.DateTimeField(blank=True)
    found = models.DateTimeField(blank=False, auto_now_add=True)
    author = models.CharField(blank=True, max_length=250)
    links = models.ManyToManyField(Link,blank=True)
    
    objects = TweetManager()
    
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"%s" % (self.raw)
