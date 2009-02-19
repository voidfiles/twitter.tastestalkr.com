# Create your views here.

from django.shortcuts import render_to_response

def filter(request,action = "last", value="24hours"):
    from twmusic.tweets.models import Tweet
    
    ranked_tweets = Tweet.objects.top_tweets(limit = 10, with_in_hours= 24)
    
    return render_to_response('base.html',
                              {"ranked_tweets":ranked_tweets} )
                              #context_instance=RequestContext(request)
