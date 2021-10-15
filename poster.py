import json
import boto3
import tweepy
import requests
import os
from content import Content
from twitter_api import twitter_api_connect
from enums import Type, Source, QueueName
from sqs_client import SQS_Client
from dynamodb_client import get_content_item, delete_content_item, DynamoDB_Client
from twitter_video_upload import post_video_status

def download_image(media_url):
    filename = '/tmp/' + 'temp.jpg'
    request = requests.get(media_url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
    return filename

def tweet_content(content):
    if isinstance(content, Content):
        twitter = twitter_api_connect()
        filename = download_image(content.media_url_list[0])
        #upload_result = twitter.media_upload(filename)
        #twitter.update_status(status="", media_ids=[upload_result.media_id_string])
        if(content.content_type == Type.IMAGE.value):
            twitter.update_with_media(filename, text="")
            print('content succesfully posted: ')
            print(content.media_url_list)
        elif(content.content_type == Type.VIDEO.value):
            # TODO: add video ability
            post_video_status(filename, text="")
            print('video successfully posted: ')
            print(content.media_url_list)
        else:
            print('unknown source_type')
        os.remove(filename)

def post_from_queue(event, context):
    sqsc = SQS_Client()
    content = sqsc.get_one_content_object_from_queue(QueueName.PREMIUM_CONTENT_QUEUE.value)
    tweet_content(content)

    result = "content tweeted"
    response = {
        "statusCode": 200,
        "body": result
    }
    return response

def to_post_or_not_to_post(event, context):
    result = 'unkown'
    new_post = json.loads(event['body'])
    print(new_post)
    if(new_post['toPost'] == '1'):
        content = get_content_item(new_post['source_link'])
        if(new_post['postNow'] == '1'):
            tweet_content(content)
            result = 'content tweeted'
        else:
            sqsc = SQS_Client()
            sqsc.send_to_queue(QueueName.PREMIUM_CONTENT_QUEUE.value, content)
            result = 'content queued'
    else:
        #delete_content_item(new_post['source_link'])
        result = 'content not posted'

    body = {
        "message": result,
        "input": new_post
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response