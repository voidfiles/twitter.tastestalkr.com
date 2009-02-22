from django.db import models
import re
# Create your models here.


songly   = re.compile("http://song.ly/\w{1,5}",re.IGNORECASE)
tinysong = re.compile("http://tinysong.com/\w{1,5}",re.IGNORECASE)
twisten  = re.compile("http://twisten.fm/l/\w{1,5}",re.IGNORECASE)
twiturm  = re.compile("http://twiturm.com/\w{1,5}",re.IGNORECASE)
trakz    = re.compile("http://tra.kz/\w+",re.IGNORECASE)
blipfm    = re.compile("http://blip.fm/~\w+",re.IGNORECASE)
twtfm    = re.compile("http://twt.fm/\w+",re.IGNORECASE)
musebin  =  re.compile("http://museb.in/\w+",re.IGNORECASE) 

TWEET_PATTERNS = [songly, tinysong, twisten, twiturm,trakz,blipfm,twtfm,musebin ]

class Link(models.Model):
    """(Links description)"""
    
    url = models.URLField(blank=False, verify_exists=False)

    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def __unicode__(self):
        return u"%s" % (self.link)
        
        
class TweetManager(models.Manager):
    
    
    def last_month(self):
        from django.core.cache import cache
        #from django.db.models import Count
        from django.db import connection
        
        cache_key = "last_24"
        #data = cache.get( cache_key)
        data = None
        if data: 
            return data
        cursor = connection.cursor()
        query = """
            SELECT count( id ) , 
                   DATE_FORMAT( found, "%s %s" ) AS day,
                   DATE_FORMAT( found, "%s%s" ) AS day_order
              FROM tweets_tweet
             WHERE found >= ((NOW( ) - INTERVAL 1 DAY) - INTERVAL 1 MONTH)
               AND found <= (NOW( ) - INTERVAL 1 DAY)
          GROUP BY day_order
          ORDER BY day_order
             LIMIT 0 , 30
        """
        cursor.execute(query,["%b","%d","%c","%d"])
        data = cursor.fetchall()
        
        maximum = 0
        for datum in data:
            if datum[0] > maximum:
                maximum = datum[0]
        csv = [unicode( ( (float(x[0])/float(maximum)) * 100  ) ) for x in data]
        csv = ",".join(csv)
        titles = [unicode(x[1]).replace("'","") for x in data]
        titles = "|".join(titles)
        
        cache.set(cache_key,(maximum,data,csv,titles),3600)
        
        
        return (maximum,data,csv,titles)

    def last_week(self):
        from django.core.cache import cache
        #from django.db.models import Count
        from django.db import connection
        
        cache_key = "last_24"
        #data = cache.get( cache_key)
        data = None
        if data: 
            return data
        cursor = connection.cursor()
        query = """
            SELECT count( id ) , 
                   DATE_FORMAT( found, "%s" ) AS day,
                   DATE_FORMAT( found, "%s" ) AS day_order
              FROM tweets_tweet
             WHERE found >= ((NOW( ) - INTERVAL 1 DAY) - INTERVAL 7 DAY)
               AND found <= (NOW( ) - INTERVAL 1 DAY)
          GROUP BY day
          ORDER BY day_order
             LIMIT 0 , 30
        """
        cursor.execute(query,["%a","%d"])
        data = cursor.fetchall()
        
        maximum = 0
        for datum in data:
            if datum[0] > maximum:
                maximum = datum[0]
        csv = [unicode( ( (float(x[0])/float(maximum)) * 100  ) ) for x in data]
        csv = ",".join(csv)
        titles = [unicode(x[1]).replace("'","") for x in data]
        titles = "|".join(titles)
        
        cache.set(cache_key,(maximum,data,csv,titles),3600)
        
        
        return (maximum,data,csv,titles)
        
        
        
    def last_24_activity(self):
        from django.core.cache import cache
        #from django.db.models import Count
        from django.db import connection
        
        cache_key = "last_24"
        #data = cache.get( cache_key)
        data = None
        if data: 
            return data
        cursor = connection.cursor()
        query = """
            SELECT count( id ) , 
                   DATE_FORMAT( found, "%s" ) AS HOUR
              FROM tweets_tweet
             WHERE found >= ( NOW( ) - INTERVAL 24 HOUR )
          GROUP BY HOUR
          ORDER BY HOUR
             LIMIT 0 , 30
        """
        cursor.execute(query,["%H"])
        data = cursor.fetchall()
        
        maximum = 0
        for datum in data:
            if datum[0] > maximum:
                maximum = datum[0]
        csv = [unicode( ( (float(x[0])/float(maximum)) * 100  ) ) for x in data]
        csv = ",".join(csv)
        titles = [unicode(x[1]).replace("'","") for x in data]
        titles = "|".join(titles)
        
        cache.set(cache_key,(maximum,data,csv,titles),3600)
        
        
        return (maximum,data,csv,titles)
        
    def top_tweets(self,limit = 10,time = None,value= None):
        import re
        import datetime
        
        from django.core.cache import cache
        #from django.db.models import Count
        from django.db import connection
        
        cache_key = "top_tweets_%s_%s_%s" % ( limit,time,value)
        tweets = cache.get( cache_key)
        if tweets: return tweets

        cursor = connection.cursor()
        query = """
            SELECT 
                   music_link, 
                   count( id ) AS count
              FROM tweets_tweet
             WHERE 
                   music_link IS NOT NULL
               AND music_link NOT LIKE ""
        """
        if time and value:
            query += "AND found >= (NOW() - INTERVAL %s %s)" % (value,time)
            
        query += """
          GROUP BY music_link
          ORDER BY count DESC
             LIMIT 0 , %s
         """  % (limit)
        cursor.execute(query)
        tweets = cursor.fetchall()

        """ 
        
        
        songs = {}
        tweets = self.all().order_by("created")
        if with_in_hours:
            date = datetime.date.today()
            date = datetime.date.today() + datetime.timedelta(hours=24)
            tweets.filter(created__gte=date)


        tweets.aggregate(Count("music_link"))

        for tweet in tweets:
            for pattern in TWEET_PATTERNS:
                matches = pattern.findall(tweet.raw)
                if len(matches) > 0:
                    if songs.get(matches[0],None):
                        songs[matches[0]] += 1
                    else:
                        songs[matches[0]] = 1
                    break
                    
                    
        alist = sorted(songs.iteritems(), key=lambda (k,v): (v,k) ,reverse=True)
        
        tweets = alist[0:limit]
        """
        
        cache.set(cache_key,tweets,600)
        
        return tweets


class Tweet(models.Model):
    """(Tweets description)"""
    raw_atom_entry = models.TextField(blank=True)
    tweet_link = models.URLField(blank=False, verify_exists=False,unique=True)
    music_link = models.URLField(blank=False, verify_exists=False)
    raw = models.TextField(blank=False)
    created = models.DateTimeField(blank=True)
    found = models.DateTimeField(blank=False, auto_now_add=True)
    author = models.CharField(blank=True, max_length=250)
    links = models.ManyToManyField(Link,blank=True)
    
    objects = TweetManager()
    
    class Admin:
        list_display = ('',)
        search_fields = ('',)

    def music_link_finder(self): 
        import re
        for pattern in TWEET_PATTERNS:
            matches = pattern.findall(self.raw)
            if len(matches) > 0:
                return matches[0]
        return None
                
                
    def __unicode__(self):
        return u"%s" % (self.raw)
