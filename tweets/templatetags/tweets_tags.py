from django import template

register = template.Library()


@register.inclusion_tag('image.html')
def google_chart(chart):
    from twmusic.tweets.models import Tweet
    image_url = "http://chart.apis.google.com/chart"
    data = {
        "chs":"430x100",
        "chtt":"Last 24 Hours",
        "cht":"bvg",
        "chbh":"12,5,6",
    }
    if chart == "last_24":
        last_24_activity = Tweet.objects.last_24_activity()
        data["chd"] = "t:%s" % (last_24_activity[2])
        data["chl"] = "0:%s" % (last_24_activity[3])
    elif chart == "last_week":
        last_week = Tweet.objects.last_week()
        data["chd"] = "t:%s" % (last_week[2])
        data["chl"] = "%s" % (last_week[3])
        data["chtt"] = "Last Week"
        data["chbh"] = "50,10,10"
    elif chart == "last_month":
        last_month = Tweet.objects.last_month()
        data["chd"] = "t:%s" % (last_month[2])
        data["chl"] = "%s" % (last_month[3])
        data["chtt"] = "Last Month"
        
    data["chtt"] = data["chtt"].replace(" ","+")
    data = "&".join(["%s=%s" % (x,data[x]) for x in data.keys()])
    image_url += "?%s" % (data) 
    return {'image_url': image_url}
