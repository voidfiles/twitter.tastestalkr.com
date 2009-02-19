from django.conf.urls.defaults import *
from twmusic.tweets.models import Tweet
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()



top_tweets = Tweet.objects.top_tweets()
index_dict = {
    'template': 'base.html',
    "extra_context":{ 
        "ranked_tweets":top_tweets 
    }
}
urlpatterns = patterns('',
    # Example:
    # (r'^twmusic/', include('twmusic.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    
    (r'^filter/(?P<action>[^/]*)/(?P<value>[^/]*)/$', 'twmusic.tweets.views.filter'),
    (r'^filter/last/(?P<time>[^/]*)/(?P<value>[^/]*)/$', 'twmusic.tweets.views.filter'),
    
    
    (r'^$', "django.views.generic.simple.direct_to_template", index_dict ),
    (r'^index.html$', "django.views.generic.simple.direct_to_template", index_dict ),
    
    
    (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
)
