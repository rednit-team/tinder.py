from tinder.entities import user, match
from tinder.entities.entity import Entity
from tinder.http import Http


class Message(Entity):
    def __init__(self, http: Http, message: dict):
        super().__init__(http, message["_id"])
        self._match_id = message["match_id"]
        self.content = message["message"]
        self.receiver_id = message["to"]
        self._author_id = message["from"]
        if "sent_date" in message:
            self.sent_date = message["sent_date"]
        else:
            self.sent_date = "N/A"
        if "timestamp" in message:
            self.timestamp = message["timestamp"]
        else:
            self.timestamp = "N/A"
        if "created_date" in message:
            self.created_date = message["created_date"]
        else:
            self.created_date = "N/A"

    def retrieve_author(self):
        route = "/user/" + self._author_id
        response = self._http.get(route).json()
        return user.User(self._http, response["results"])

    def retrieve_match(self):
        route = "/v2/matches/" + self._match_id
        response = self._http.get(route).json()
        return match.Match(self._http, response["data"])
