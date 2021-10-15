class User():
    user_id = ""
    following = False
    follow_back = False

    def __init__(self, user_id, following, follow_back):
        self.user_id = user_id
        self.following = following
        self.follow_back = follow_back