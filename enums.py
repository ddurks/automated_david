from enum import Enum

class Type(Enum):
    IMAGE = 'image'
    VIDEO = 'video'
    IMAGE_LIST = 'image_list'

class Source(Enum):
    TWITTER = 'twitter'
    REDDIT = 'reddit'
    TUMBLR = 'tumblr'
    INSTAGRAM = 'instagram'

class ToPost(Enum):
    NOPOST = 0
    POST = 1

class QueueURL(Enum):
    REVIEW_QUEUE = 'https://sqs.us-east-1.amazonaws.com/593615615124/review_queue'
    PREMIUM_CONTENT_QUEUE = 'https://sqs.us-east-1.amazonaws.com/593615615124/ultimate_premium_content_queue'

class QueueName(Enum):
    REVIEW_QUEUE = 'review_queue'
    PREMIUM_CONTENT_QUEUE = 'ultimate_premium_content_queue'

class EnumMapper():
    def contentType(self, type_str):
        if (type_str == 'image'):
            return Type.IMAGE
        elif (type_str == 'video'):
            return Type.VIDEO
        elif (type_str == 'image_list'):
            return Type.IMAGE_LIST
        else:
            return None
    def sourceType(self, type_str):
        if (type_str == 'twitter'):
            return Source.TWITTER
        elif (type_str == 'reddit'):
            return Source.REDDIT
        elif (type_str == 'tumblr'):
            return Source.TUMBLR
        elif (type_str == 'instagram'):
            return Source.INSTAGRAM
        else:
            return None