from twitter_api import twitter_api_connect
import tweepy
from dynamodb_client import DynamoDB_Client
from content_creator import Content_Creator
from enums import Source

def refresh_content_creators(event, context):
    twitter = twitter_api_connect()
    dbc = DynamoDB_Client()
    dbc.user_client()

    new_ccs = 0
    me = twitter.me()
    for user in tweepy.Cursor(twitter.friends, id=me.id, wait_for_rate_limit=True).items():
      dbc.content_creator_client()
      content_creator = Content_Creator(str(user.id), Source.TWITTER.value, user.screen_name, 0, 0, 0, 0)
      dbc.save_content_creator(content_creator)
      new_ccs = new_ccs + 1
      print('saved ' + str(user.screen_name) + ' as a content creator')
    print('added ' + str(new_ccs) + ' new content creators')

if __name__ == '__main__':
  refresh_content_creators(None, None)
