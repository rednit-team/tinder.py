from tinder.http import Http


class Entity:
    def __init__(self, http: Http, entity_id: str):
        self._http = http
        self.entity_id = entity_id
