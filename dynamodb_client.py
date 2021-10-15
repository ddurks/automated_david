import boto3
import json
from dynamodb_mapper import to_dynamodb, from_dynamodb
from content import Content
from sqs_client import content_decoder
from content_creator import Content_Creator
from boto3.dynamodb.conditions import Key, Attr
from user import User

class DynamoDB_Client():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
    def content_client(self):
        self.table = self.dynamodb.Table('automated_david_posts')
    def save_content(self, content):
        if isinstance(content, Content):
            try:
                self.table.put_item(
                        Item=content.__dict__,
                        ConditionExpression='attribute_not_exists(source_link)'
                    )
                return True
            except Exception as e:
                print(e)
                return False

    def get_content_to_post(self, content):
        response = self.table.query(
            KeyConditionExpression=Key('source_link').eq(c)
        )
        items = response['Items']
        if(items):
            c_dict = items[0]
            user = User(c_dict['user_id'], c_dict['following'], c_dict['follow_back'])
            if(isinstance(user, User)):
                return user
        else:
            print('query failed user_id=' + str(user_id))
            return None
    def content_creator_client(self):
        self.table = self.dynamodb.Table('content_creators')
    def save_content_creator(self, content_creator):
        if isinstance(content_creator, Content_Creator):
            try:
                self.table.put_item(Item=content_creator.__dict__, ConditionExpression='attribute_not_exists(user_id)')
                return True
            except Exception as e:
                print('noupload')
                print(e)
                return False
    def get_content_creators(self):
        response = self.table.scan()
        items = response['Items']
        content_creators = []
        if(items):
            for c_dict in items:
                content_creator = Content_Creator(c_dict['user_id'], c_dict['source_type'], c_dict['screen_name'], c_dict['avg_retweets'], c_dict['avg_likes'], c_dict['avg_replies'], c_dict['tweets_analyzed'])
                if isinstance(content_creator, Content_Creator):
                    content_creators.append(content_creator)
            return content_creators
        else:
            #print(str(user_id) + ',')
            return None

    def user_client(self):
        self.table = self.dynamodb.Table('automated_david_teamfollowback')
    def save_user(self, user):
        if isinstance(user, User):
            try:
                self.table.put_item(Item=user.__dict__, ConditionExpression='attribute_not_exists(user_id)')
                return True
            except Exception as e:
                print('noupload')
                print(e)
                return False
    def update_user(self, user):
        if isinstance(user, User):
            try:
                self.table.put_item(Item=user.__dict__)
                return True
            except Exception as e:
                print('noupload')
                print(e)
                return False        
    def get_all_users(self):
        response = self.table.scan()
        items = response['Items']
        content_creators = []
        if(items):
            for c_dict in items:
                content_creator = Content_Creator(c_dict['user_id'], c_dict['source_type'], c_dict['screen_name'], c_dict['avg_retweets'], c_dict['avg_likes'], c_dict['avg_replies'], c_dict['tweets_analyzed'])
                if isinstance(content_creator, Content_Creator):
                    content_creators.append(content_creator)
            return content_creators
        else:
            #print(str(user_id) + ',')
            return None
    def get_user(self, user_id):
        response = self.table.query(
            KeyConditionExpression=Key('user_id').eq(str(user_id))
        )
        items = response['Items']
        if(items):
            c_dict = items[0]
            user = User(c_dict['user_id'], c_dict['following'], c_dict['follow_back'])
            if(isinstance(user, User)):
                return user
        else:
            print('query failed user_id=' + str(user_id))
            return None

    def get_non_followers(self):
        response = self.table.scan()
        items = response['Items']
        user_list = []
        if(items):
            for c_dict in items:
                user = User(c_dict['user_id'], c_dict['following'], c_dict['follow_back'])
                if(isinstance(user, User)):
                    user_list.append(user)
            return user_list
        else:
            print('query failed')
            return None
    def team_followback(self, user_id):
        response = self.table.query(
            KeyConditionExpression=Key('user_id').eq(str(user_id))
        )
        items = response['Items']
        if(items):
            c_dict = items[0]
            user = User(c_dict['user_id'], c_dict['following'], c_dict['follow_back'])
            if(isinstance(user, User)):
                return user
        else:
            #print(str(user_id) + ',')
            return None

def delete_content_item(source_link):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('automated_david_posts')
    response = ""
    try:
        response = table.delete_item(
            TableName='automated_david_posts',
            Key={
                'source_link' : source_link
            }
        )
    except Exception as e:
        print(e)
    print(response)
    
def get_content_item(source_link):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('automated_david_posts')
    response = table.query(
        KeyConditionExpression=Key('source_link').eq(str(source_link))
    )
    items = response['Items']
    if(items):
        c_dict = items[0]
        content = Content(c_dict['id'], c_dict['content_type'], c_dict['source_type'], c_dict['source_link'], c_dict['text'], c_dict['media_url_list'])
        if(isinstance(content, Content)):
            return content
    else:
        print('query failed source_link=' + source_link)

def clear_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('automated_david_posts')
    scan = table.scan()
    with table.batch_writer() as batch:
        count = 0
        while scan is None or 'LastEvaluatedKey' in scan:
            if scan is not None and 'LastEvaluatedKey' in scan:
                scan = table.scan(
                    ProjectionExpression='source_link',
                    ExclusiveStartKey=scan['LastEvaluatedKey'],
                )
            else:
                scan = table.scan(ProjectionExpression='source_link')

            for item in scan['Items']:
                if count % 5000 == 0:
                    print(count)
                batch.delete_item(Key={'source_link': item['source_link']})
                print(item)
                print(count)
                count = count + 1
if __name__ == "__main__":
    content = {'toPost': '0', 'source_link': 'https://i.redd.it/ojrz8dmyfda41.jpg', 'postNow': '0'}
    delete_content_item(content['source_link'])