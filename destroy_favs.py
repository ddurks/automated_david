from twitter_api import twitter_api_connect
import tweepy

def destroy_faves(event, context):
    twitter = twitter_api_connect()

    me = twitter.me()
    for page in tweepy.Cursor(twitter.favorites,id=me.id,wait_on_rate_limit=True, count=200).pages(200):
        for status in page:
            twitter.destroy_favorite(id=status.id)
            print('destroyed fav on status #' + str(status.id))