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
        
        songs = Tweet.objects.top_tweets(limit=30)
                    
                        
        for song in songs:
            print "%s %s" % (song[1],song[0])
        
                    
            
                
            

        
        
        
        
