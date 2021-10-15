import generator
import poster
import fetcher
from content import Content
from dynamodb_mapper import to_dynamodb, from_dynamodb
from dynamodb_client import DynamoDB_Client, get_content_item
from enums import Type, Source, ToPost
from twitter_api import twitter_api_connect
from sqs_client import SQS_Client
from enums import QueueURL
import json
import uuid
from team_followback import team_followback, team_followback_luv, team_followback_cleanup, cleanup_likes
import time
import tweepy
from refresh_content_creators import refresh_content_creators

if __name__ == '__main__':
    #generator.generate_premium_content(None, None)
    #poster.to_post_or_not_to_post(None, None)
    '''
    url_list = ['url']
    content = Content(str(uuid.uuid4()), Type.IMAGE.value, Source.TWITTER.value, 'link', 'text', url_list)
    
    contentstr = json.dumps(content.__dict__)
    print(contentstr)
    backtocontent = json.loads(contentstr)

    encoder = ContentJSONEncoder()
    print(encoder.encode(content))
    print(json.loads(encoder.encode(content)))

    sqsg = SQS_Client()
    content = sqsg.get_one_message_from_queue(QueueURL.REVIEW_QUEUE)
    print(content.media_url_list[0])

    cs = DynamoDB_Client()
    cs.save_content(content)
    print(from_dynamodb(get_content_item(content.source_link)).media_url_list[0])

    event = { "newPost" : {"source_link" : "https://twitter.com/DankRedditMeme/status/1155923073696186368", "toPost" : "1", "postNow": "0"} }
    poster.to_post_or_not_to_post(event, None)

    generator.generate_premium_content(None, None)

    fetcher.fetch_premium_content(None, None)

    poster.post_from_queue(None, None)
    '''
    #team_followback_cleanup(None, None)
    sqs_client = SQS_Client()
    sqs_client.get_queue_size(queue_url=QueueURL.REVIEW_QUEUE.value)
