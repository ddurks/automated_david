import json
import tweepy
from twitter_api import twitter_api_connect, get_tweet_url
from content import Content
from enums import Type, Source, QueueName
from dynamodb_client import DynamoDB_Client
from sqs_client import SQS_Client
import uuid
import praw
import credentials
from random import shuffle

def generate_premium_reddit_content():
    reddit = praw.Reddit(client_id=credentials.REDDIT_CLIENT_ID,
                     client_secret=credentials.REDDIT_CLIENT_SECRET,
                     user_agent=credentials.REDDIT_USER_AGENT,
                     username=credentials.REDDIT_USERNAME,
                     password=credentials.REDDIT_PASSWORD)
    
    content_list = []
    for subreddit in list(reddit.user.subreddits(limit=None)):
        content_num = 0
        for submission in reddit.subreddit(str(subreddit)).top('day', limit=5):
            if content_num < 5:
                media_urls = []
                try:
                    if(submission.media != None):
                        print(submission.media['reddit_video'])
                except KeyError as e:
                    pass
                
                if submission.url.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print("reddit url:" + submission.url.lower())
                    media_urls.append(str(submission.url))
                    content = Content(str(submission.url), Type.IMAGE.value, Source.REDDIT.value, str(submission.url), str(submission.title), media_urls)
                    print(content.source_link)
                    content_list.append(content)
                    content_num=content_num+1
            else:
                break
    return content_list

def generate_premium_twitter_content():
    twitter = twitter_api_connect()
    cs = DynamoDB_Client()

    content_list = []
    total_tweets = 0
    try:
        cs.content_creator_client()
        for content_creator in cs.get_content_creators():
            user = twitter.get_user(id=content_creator.user_id)
            for tweet in twitter.user_timeline(id=user.id, count=10):
                image_urls = []
                media_type = Type.IMAGE.value
                if 'media' in tweet.entities:
                    total_tweets+=1
                    if tweet.extended_entities is not None:
                        if 'media' in tweet.extended_entities:
                            for media in tweet.extended_entities['media']:
                                # TODO: allow extended_media photo arrays
                                if media['type'] == 'video':
                                    #print("video link: " + media['video_info']['variants'][0]['url'])
                                    media_type = Type.VIDEO.value
                                    hi_bitrate = 0
                                    video_url = ''
                                    for video in media['video_info']['variants']:
                                        if 'bitrate' in video and video['bitrate'] > hi_bitrate:
                                            hi_bitrate = video['bitrate']
                                            video_url = video['url']
                                    if video_url == '':
                                        video_url = media['video_info']['variants'][0]['url']
                                    else:
                                        image_urls.append(video_url)
                                else:
                                    first_url = ""
                                    if media['type'] == 'photo':
                                        image_urls.append(media['media_url'])
                                        first_url = media['media_url']
                                    if media['type'] == 'animated_gif':
                                        image_urls.append(media['video_info']['variants'][0]['url'])
                                    if tweet.entities is not None:
                                        for image in tweet.entities['media']:
                                            if len(image_urls) < 4 and image['media_url'] != first_url:
                                                image_urls.append(image['media_url'])
                                            #print("image link: " + image['media_url'])
                if (len(image_urls) == 1):
                    content = Content(str(uuid.uuid4()), media_type, Source.TWITTER.value, get_tweet_url(tweet), tweet.text, image_urls)
                    print(content.source_link)
                    content_list.append(content)
    except tweepy.error.TweepError as e:
        print('failure generating twitter content:' + str(e))

    return content_list 

def generate_premium_content(event, context):
    result = 'unknown'
    sqsc = SQS_Client()
    cs = DynamoDB_Client()
    cs.content_client()

    content_list = []
    twitter_content_list = generate_premium_twitter_content()
    reddit_content_list = generate_premium_reddit_content()
    content_list.extend(twitter_content_list)
    content_list.extend(reddit_content_list)
    print('added ' + str(len(twitter_content_list)) + ' tweets and ' + str(len(reddit_content_list)) + ' reddit posts')
    shuffle(content_list)

    print('adding to review_queue')
    count = 0
    for content in content_list:
        if cs.save_content(content):
            sqsc.send_to_queue(QueueName.REVIEW_QUEUE.value, content)
            count+=1
    print(count)



    #print("Total Tweets: " + str(total_tweets))
    #print("Average Like Ratio: " + str(float(running_sum)/float(total_tweets)))
    body = {
        "message": result,
        "input": event
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

if __name__ == '__main__':
  generate_premium_content(None, None)