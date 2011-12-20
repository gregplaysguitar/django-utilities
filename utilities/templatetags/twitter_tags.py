import urllib2, httplib
from ftplib import FTP

from django import template
import twitter
from BeautifulSoup import BeautifulSoup

from utilities.helpers import cached
from utilities.easy_tag import easy_tag


register = template.Library()



class TweetNode(template.Node):
    def __init__(self, username, varname, favourite=False):
        self.username = username
        self.varname = varname
        self.favourite = favourite
    
    def render(self, context):
        username = template.Variable(self.username).resolve(context)
        
        @cached('latest-tweet-%s' % username, 60 * 30)
        def get_latest_tweet():
            try:
                client = twitter.Api()
                if self.favourite:
                    tweets = client.GetFavorites(username)
                    if not len(tweets):
                        tweets = client.GetUserTimeline(username)
                    for status in tweets:
                        if status.user.screen_name.lower() == username.lower():
                            return status
                else:
                    tweets = client.GetUserTimeline(username)
                    if len(tweets):
                        return tweets[0]

            except (urllib2.URLError, httplib.BadStatusLine), e:
                pass
            return None

        context[self.varname] = get_latest_tweet()
        return ''
        
        
@register.tag
@easy_tag
def get_latest_tweet(_tag, _from, username, _as, varname):
    return TweetNode(username, varname)


@register.tag
@easy_tag
def get_favourite_tweet(_tag, _from, username, _as, varname):
    return TweetNode(username, varname, True)
