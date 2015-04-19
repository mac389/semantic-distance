import tweepy, json, sys
from twython import Twython


keys = json.load(open('../../data/keys.json','rb'))
auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
auth.set_access_token(keys['access_token'], keys['access_token_secret'])


twitter = Twython(keys['consumer_key'],keys['consumer_secret'],keys['access_token'],keys['access_token_secret'])
tweet = twitter.request(endpoint='showStatus',
          params={id:86383662232375296})

print tweet
'''
api = tweepy.API(auth,wait_on_rate_limit_notify=True, wait_on_rate_limit=True)

#86383662232375296
tweet_ids = []
with open('../../../fsd_corpus/tweet_ids') as f:
    for line in f:
		tweet_id,_ = line.split()
		tweet_id = tweet_id.strip()

		while len(tweet_ids)<100:
			tweet_ids += [tweet_id]

		if len(tweet_ids) == 100:
			tweets = api.statuses_lookup([tweet_ids])
			with open('../../data/tweets','a+') as outfile:
				for tweet in tweets:
					print>>outfile,tweet.text
					print line 
			tweet_ids = []
'''