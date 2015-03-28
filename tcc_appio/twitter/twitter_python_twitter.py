import twitter


consumer_key="MeDoUEP9VCCBdObR4aEmgaSnZ"
consumer_secret="R8cMBDCOqbhbfkrY9gJxosnwmFX5RhO8QptxxzZhgBQunzah4N"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="3097855917-oD9PXc4ahK8wcWoRortjVldutNVonMPVzwCf8Ka"
access_token_secret="lB2VwSuKLPnZ7pb6JOIn2GwHTAl8UGbyAuqlFfzD09Ggb"


api = twitter.Api(consumer_key,consumer_secret,access_token,access_token_secret)
#users = api.GetFriends()
#friends = api.GetFriends()

x = api.GetHomeTimeline()

user = api.GetUser(494465681)
print user.status.text

#ids = api.GetFriendIDs()

#for i in ids:
 #   print i


#print [u.name for u in users]