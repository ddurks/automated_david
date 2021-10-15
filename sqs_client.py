import boto3
from enums import QueueName, EnumMapper
from dynamodb_mapper import to_dynamodb, from_dynamodb
import json
import ast
from content import Content
from collections import namedtuple

def content_decoder(c_dict):
    return Content(c_dict['id'], c_dict['content_type'], c_dict['source_type'], c_dict['source_link'], c_dict['text'], c_dict['media_url_list'])

class SQS_Client():
    def __init__(self):
        self.sqs = boto3.resource('sqs')
        self.sqs_client = boto3.client('sqs')
    def send_to_queue(self, queue_name, content):
        queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        queue.send_message(MessageBody=json.dumps(content.__dict__))
    def get_one_content_object_from_queue(self, queue_name):
        queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        for message in queue.receive_messages():
            content = json.loads(message.body, object_hook=content_decoder)
            message.delete()
            return content
    def get_content_from_queue(self, queue_name, queue_url):
        queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        content_list = []
        delete_batch = []
        for message in queue.receive_messages(MaxNumberOfMessages=10):
            content = json.loads(message.body, object_hook=content_decoder)
            if(isinstance(content, Content)):
                content_list.append(content)
                delete_batch.append({'Id': message.message_id,'ReceiptHandle': message.receipt_handle})
        if delete_batch:
            self.sqs_client.delete_message_batch(QueueUrl=queue_url, Entries=delete_batch)
        print(content_list)
        return content_list
    def get_queue_size(self, queue_url):
        response = self.sqs_client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['ApproximateNumberOfMessages']
        )
        return response['Attributes']['ApproximateNumberOfMessages']
    def clear_queue(self, queue_name):
        queue = self.sqs.get_queue_by_name(QueueName=queue_name)
        queue.purge()
