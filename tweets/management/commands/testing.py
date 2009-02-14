from django.core.management.base import BaseCommand, CommandError
from django.core import serializers

from optparse import make_option


def handle_listen_to(tweet):
    """example Listening to Pretty Girl Why by Buffalo Springfield on <b>Twisten</b>.FM - <a href="http://twisten.fm/l/2UnQ">http://<b>twisten</b>.fm/l/2UnQ</a>"""
    print tweet
    return True
    
def handle_just_listened_to(tweet):
    """example just listened to Into the Night (feat. Chad Kroeger) by Santana on Grooveshark: <a href="http://tinysong.com/2UC7">http://<b>tinysong.com</b>/2UC7</a>"""
    print tweet
    return True
        
class Command(BaseCommand):
    """ 
    option_list = BaseCommand.option_list + (
        make_option('--search', default=None, dest='search', help='What are you searching on twitter'),
    )
    help = 'Add tweets for a given search'
    args = 'search'
    
    example urls: 
    http://song.ly/7ly
    http://tinysong.com/2UDC - last 4 are the same 
    http://twisten.fm/l/2UDy - last 4 are the same 
    http://twiturm.com/emrg
    http://tra.kz/mss9
    
    """

    def handle(self, *app_labels, **options):
        from tweets.models import Tweet 
        import re
        
        songs = {}
        tweets = Tweet.objects.all().order_by("created")
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
        
        print alist[0:10]
        
                    
            
                
            

        
        
        
        
