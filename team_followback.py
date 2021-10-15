from twitter_api import twitter_api_connect
from dynamodb_client import DynamoDB_Client
from random import randrange
from user import User
from content_creator import Content_Creator
import tweepy
import time
from enums import Source
import json
from random import shuffle

def team_followback_favbomb(event, context):
    result = 'unknown'
    twitter = twitter_api_connect()
    dbc = DynamoDB_Client()

    me = twitter.me()
    users_faved_total = 0
    total_faves = 0
    dbc.content_creator_client()
    content_creators = dbc.get_content_creators()
    while total_faves < 10:
        rand_index = randrange(0, len(content_creators))
        content_creator = content_creators[rand_index]
        print(content_creator.user_id)
        user = twitter.get_user(id=content_creator.user_id)
        selection_num=0               
        for _id in tweepy.Cursor(twitter.followers_ids, id=user.id).items():
            if selection_num > 10:
                break
            potential_follow = twitter.get_user(_id)
            if(not potential_follow.protected):
                i=0
                for tweet in twitter.user_timeline(id=_id, count=randrange(1,10)):
                    if(not tweet.favorited and not hasattr(tweet, 'retweeted_status')):
                        twitter.create_favorite(id=tweet.id)
                        total_faves+=1
                        i+=1
                print('faved ' + str(i) + ' tweets from @' + potential_follow.screen_name)
                if(_id != me.id):
                    user = User(str(_id), True, False)
                    users_faved_total+=1
                    selection_num+=1
    
    result = 'fav bombed ' + str(users_faved_total) + ' new users, faved ' + str(total_faves) + ' new tweets...'
    print(result)
    
    body = {
        "message": result,
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

def team_followback_followerluv(event, context):
    result = 'unknown'
    twitter = twitter_api_connect()
    dbc = DynamoDB_Client()
    dbc.user_client()
    me = twitter.me()
    # team_followback_luv
    print('#TFBLuv')
    for _id in tweepy.Cursor(twitter.followers_ids, id=me.id).items():
        user = twitter.get_user(id=_id)
        print('@' + user.screen_name)
        if(not user.protected):
            i=0
            tweets=0
            for tweet in twitter.user_timeline(id=_id, count=randrange(1,5)):
                tweets+=1
                if(not tweet.favorited and not hasattr(tweet, 'retweeted_status')):
                    twitter.create_favorite(id=tweet.id)
                    i=i+1
            result = 'faved ' + str(i) + ' tweets from @' + user.screen_name
            print(result)
    response = {
        "statusCode": 200,
        "body": result
    }

    return response

def team_followback_cleanup(event, context):
    result = 'unknown'
    twitter = twitter_api_connect()
    dbc = DynamoDB_Client()
    dbc.user_client()
    me = twitter.me()
    new_tfb = 0
    '''
    for _id in tweepy.Cursor(twitter.followers_ids, id=me.id).items():
        friendship = twitter.show_friendship(source_id=me.id, target_id=_id)
        if(friendship[0].following):
            try:
                tfb_user = dbc.get_user(user_id=_id)
            except Exception as e:
                print(e)
            if(tfb_user != None and tfb_user.follow_back == False):
                tfb_user.follow_back = True
                dbc.update_user(tfb_user)
                new_tfb=new_tfb+1
                user_object = twitter.get_user(id=_id)
                print('new #TFB user! ' + user_object.screen_name)

    print(str(new_tfb) + ' new TFB members')
    '''
    flwrs = dbc.get_non_followers()
    shuffle(flwrs)
    users_unfollowed = 0
    for user in flwrs:
        if users_unfollowed > 49:
            break
        if (user.following == True and user.follow_back == False):
            try:
                twitter.destroy_friendship(id=user.user_id)
                print('unfollowed a user...')
                users_unfollowed=users_unfollowed+1
            except Exception as e:
                print(e)

    result = 'unfollowed ' + str(users_unfollowed) + ' users'
    print(result)
    response = {
        "statusCode": 200,
        "body": result
    }

    return response
    
def cleanup_likes(event, context):
    twitter = twitter_api_connect()
    dbc = DynamoDB_Client()
    dbc.user_client()
    me = twitter.me()
    tweets_unfaved = 0
    for fav in tweepy.Cursor(twitter.favorites, id=me.id, count=25).items():
        if tweets_unfaved < 100:
            try:
                twitter.destroy_favorite(fav.id)
                print('unfaved a tweet...')
                tweets_unfaved = tweets_unfaved+1
            except Exception as e:
                print(e)
        else:
            break
    print('unfaved ' + str(tweets_unfaved) + ' tweets!')

if __name__ == "__main__":
    cleanup_likes(None, None)