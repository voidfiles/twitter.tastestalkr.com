from django.core.management.base import BaseCommand, CommandError
from django.core import serializers

from optparse import make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--search', default=None, dest='search', help='What are you searching on twitter'),
    )
    help = 'Add tweets for a given search'
    args = 'search'

    def handle(self, *app_labels, **options):
        from tweets.models import Tweet 
        import httplib2 
        import feedparser
        import pprint 
        import pickle
        import datetime
        search = options.get('search',None)
        if not search:
            print "need a search term"
            exit()
        show_traceback = options.get('traceback', False)
        
        search_url = "http://search.twitter.com/search.atom?q="
        h = httplib2.Http()
        resp, content = h.request(search_url + search)
        
        d = feedparser.parse(content)
        


        for entry in d.entries:
            
            raw_entry = pickle.dumps(entry)
            raw_entry = raw_entry.encode('base64')
            raw_entry = unicode(raw_entry)
            
            raw_content = entry.content[0]["value"]
            created = datetime.datetime(
                entry.published_parsed[0],
                entry.published_parsed[1],
                entry.published_parsed[2],
                entry.published_parsed[3],
                entry.published_parsed[4],
                entry.published_parsed[5],
            )
            tweet_link = entry.link
            author = entry.author
            try:
                tweet = Tweet.objects.get(tweet_link=tweet_link)
            except Tweet.DoesNotExist:
                tweet = Tweet.objects.create(
                    raw_atom_entry=raw_entry,
                    raw=raw_content,
                    created=created,
                    tweet_link=tweet_link,
                    author=author,
                )
            
        
        
        
        
