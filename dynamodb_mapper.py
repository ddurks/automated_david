from content import Content
import boto3
import json

def to_dynamodb(content):
    if isinstance(content, Content):
        Item = {
            'id' : content.id,
            'content_type' : content.content_type,
            'source_type' : content.source_type,
            'source_link' : content.source_link,
            'text' : content.text,
            'media_url_list' : content.media_url_list
        }
        return Item
    else:
        return None

def from_dynamodb(item_dict):
    return (item_dict['id'], item_dict['content_type'], item_dict['source_type'], item_dict['source_link'], item_dict['text'], json.loads(item_dict['media_url_list']) )



  