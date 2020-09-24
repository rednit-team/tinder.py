class FacebookInfo:
    __slots__ = [
        "common_connections",
        "connection_count",
        "common_interests",
        "common_likes",
        "common_like_count",
        "common_friends",
        "common_friend_count"
    ]

    def __init__(self, facebook: dict):
        self.common_connections = facebook["common_connections"]
        self.connection_count = facebook["connection_count"]
        self.common_interests = facebook["common_interests"]
        self.common_likes = facebook["common_likes"]
        self.common_like_count = facebook["common_like_count"]
        self.common_friends = facebook["common_friends"]
        self.common_friend_count = facebook["common_friend_count"]
