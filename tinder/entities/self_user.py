from tinder.entities import entity
from tinder.http import Http


class SelfUser(entity.Entity):
    __slots__ = [
        "age_filter_min",
        "age_filter_max",
        "birth_date",
        "create_date",
        "discoverable",
        "_distance_filter",
        "email",
        "photo_optimizer_enabled",
        "can_create_squad",
        "gender_filter"
    ]

    def __init__(self, http: Http, user: dict):
        super().__init__(http, user["_id"])
        self.age_filter_min = user["age_filter_min"]
        self.age_filter_max = user["age_filter_max"]
        self.birth_date = user["birth_date"]
        self.create_date = user["create_date"]
        self.discoverable = user["discoverable"]
        self._distance_filter = user["distance_filter"]
        self.email = user["email"]
        self.photo_optimizer_enabled = user["photo_optimizer_enabled"]
        self.can_create_squad = user["can_create_squad"]
        self.gender_filter = user["gender_filter"]

    def distance_filter_mi(self):
        return self._distance_filter

    def distance_filter_km(self):
        return self._distance_filter * 1.609344

    def update_search_preferences(self, **kwargs):
        self._http.post("/v2/profile", {"user": kwargs})
        for key in kwargs.keys():
            self.__setattr__(key, kwargs.get(key))

    def update_job(self, company: str, title: str):
        self._http.post("/v2/profile/job",
                        {"jobs": {"company": {"displayed": bool(company), "name": company},
                                  "title": {"displayed": bool(title), "name": title}}})

    def update_bio(self, bio: str):
        self._http.post("/v2/profile", {"user": {"bio": bio}})

    def update_gender(self, gender: int, show_gender: bool):
        self._http.post("/v2/profile",
                        {"user": {"show_gender_on_profile": show_gender, "gender": gender}})

    def update_sexual_orientation(self, show_orientation, **kwargs):
        self._http.post("/v2/profile",
                        {"user": {"show_orientation_on_profile": show_orientation,
                                  "sexual_orientations": kwargs}})

    def change_school(self, name: str, school_id: str):
        self._http.post("/v2/profile/school",
                        {"schools": {"displayed": True, "name": name, "school_id": school_id}})

    def reset_school(self):
        self._http.post("/v2/profile/school", {"schools": {}})

    def change_city(self, **kwargs):
        self._http.post("/v2/profile/city", kwargs)

    def reset_city(self):
        self._http.delete("/v2/profile/city")

    def change_interests(self, **kwargs):
        self._http.post("/v2/profile", {"user": {"user_interests": {"selected_interests": kwargs}}})

    def reset_interests(self):
        self._http.delete("/v2/profile/userinterests")

    def passport_to_location(self, lat, long):
        self._http.post("/passport/user/travel", {"lat": lat, "long": long})

    def reset_passport(self):
        self._http.post("/passport/user/reset")

    def update_location(self, lat, long):
        self._http.post("/user/ping", {"lat": lat, "long": long})

    def like_count(self) -> int:
        return self._http.get("/v2/fast-match/count").json()["data"]["count"]
