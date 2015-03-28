import tweepy

# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="MeDoUEP9VCCBdObR4aEmgaSnZ"
consumer_secret="R8cMBDCOqbhbfkrY9gJxosnwmFX5RhO8QptxxzZhgBQunzah4N"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="3097855917-oD9PXc4ahK8wcWoRortjVldutNVonMPVzwCf8Ka"
access_token_secret="lB2VwSuKLPnZ7pb6JOIn2GwHTAl8UGbyAuqlFfzD09Ggb"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print 'Error! Failed to get request token.'
    
api = tweepy.API(auth)

print api.list_timeline()



#for status in tweepy.Cursor(api.user_timeline).items(200):
 #   print status