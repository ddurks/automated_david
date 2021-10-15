import json
from sqs_client import SQS_Client, content_decoder
from enums import QueueName, QueueURL
from content import Content

def fetch_premium_content(event, context):
    sqsc = SQS_Client()
    content_objs = sqsc.get_content_from_queue(QueueName.REVIEW_QUEUE.value, QueueURL.REVIEW_QUEUE.value)
    queue_size = sqsc.get_queue_size(QueueURL.REVIEW_QUEUE.value)

    content_list = []
    for content in content_objs:
        content_dict = content.__dict__
        content_list.append(content_dict)

    response_body = {
        "queue_size" : json.dumps(queue_size),
        "content_list": content_list
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }
    '''
    content_list = json.loads(response_body)

    for content_obj_str in content_list:
        content = content_decoder(content_obj_str)
        print(content.media_url_list)
    '''
    return response

def purge_review_queue(event, context):
    sqsc = SQS_Client()
    sqsc.clear_queue(QueueName.REVIEW_QUEUE.value)

if __name__ == "__main__":
    purge_review_queue(None, None)