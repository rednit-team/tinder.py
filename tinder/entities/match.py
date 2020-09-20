from typing import Tuple

from tinder.entities import entity, user, message
from tinder.http import Http


class Match(entity.Entity):
    __slots__ = ["closed",
                 "common_friend_count",
                 "common_like_count",
                 "created_date",
                 "dead",
                 "last_activity_date",
                 "pending",
                 "is_super_like",
                 "is_boost_match",
                 "is_super_boost_match",
                 "is_experiences_match",
                 "is_fast_match",
                 "is_opener",
                 "_user_id"]

    def __init__(self, http: Http, match: dict):
        super().__init__(http, match["_id"])
        self.closed = match["closed"]
        self.common_friend_count = match["common_friend_count"]
        self.common_like_count = match["common_like_count"]
        self.created_date = match["created_date"]
        self.dead = match["dead"]
        self.last_activity_date = match["last_activity_date"]
        self.pending = match["pending"]
        self.is_super_like = match["is_super_like"]
        self.is_boost_match = match["is_boost_match"]
        self.is_super_boost_match = match["is_super_boost_match"]
        self.is_experiences_match = match["is_experiences_match"]
        self.is_fast_match = match["is_fast_match"]
        self.is_opener = match["is_opener"]
        self._user_id = match["person"]["_id"]

    def retrieve_user(self):
        route = "/user/" + self._user_id
        response = self._http.get(route).json()
        return user.User(self._http, response["results"])

    def send_message(self, content: str) -> message.Message:
        route = "/user/matches/{}".format(self.entity_id)
        response = self._http.post(route, {"message": content}).json()
        return message.Message(self._http, response)

    def retrieve_messages(self,
                          count: int = 60,
                          page_token: str = None) -> Tuple[message.Message, ...]:
        route = "/v2/matches/{}/messages?count={}".format(self.entity_id, count)
        if page_token:
            route = route + "&page_token=" + page_token
        response = self._http.get(route).json()
        messages = list()
        for msg in response["data"]["messages"]:
            messages.append(message.Message(self._http, msg))
        return tuple(messages)
