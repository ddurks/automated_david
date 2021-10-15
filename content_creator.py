from enums import Source
class Content_Creator():
    user_id = ""
    source_type = ""
    screen_name = ""
    avg_retweets = 0
    avg_likes = 0
    avg_replies = 0
    tweets_analyzed = 0

    def __init__(self, user_id, source_type, screen_name, avg_retweets, avg_likes, avg_replies, tweets_analyzed):
        self.user_id = user_id
        self.source_type = source_type
        self.screen_name = screen_name
        self.avg_likes = avg_likes
        self.avg_retweets = avg_retweets
        self.avg_replies = avg_replies
        self.tweets_analyzed = tweets_analyzed