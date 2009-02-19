# Create your views here.

from django.shortcuts import render_to_response

def filter(request,time = "hour", value="24"):
    from twmusic.tweets.models import Tweet
    ACCEPTABLE_TIMES = [
        "hour",
        "day",
        "month",
        "second",
        "week",
        "year",
    ]
    assert time.lower() in ACCEPTABLE_TIMES, "%s is not a support paramater" % (time)
    
    value = int(value)
    ranked_tweets = Tweet.objects.top_tweets(limit = 10, time = time, value= value)
    
    return render_to_response('base.html',
                              {"ranked_tweets":ranked_tweets} )
                              #context_instance=RequestContext(request)
