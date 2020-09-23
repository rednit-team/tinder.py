from typing import Tuple

from tinder.entities import entity
from tinder.http import Http


class SelfUser(entity.Entity):
    __slots__ = ["age_filter_min",
                 "age_filter_max",
                 "badges",
                 "bio",
                 "birth_date",
                 "create_date",
                 "discoverable",
                 "_distance_filter",
                 "email",
                 "gender",
                 "photo_optimizer_enabled",
                 "ping_time",
                 "show_gender_on_profile",
                 "can_create_squad",
                 "job_title",
                 "company",
                 "school",
                 "city",
                 "interests"]

    def __init__(self, http: Http, user: dict):
        super().__init__(http, user["_id"])
        self.age_filter_min = user["age_filter_min"]
        self.age_filter_max = user["age_filter_max"]
        self.badges = user["badges"]
        self.bio = user["bio"]
        self.birth_date = user["birth_date"]
        self.create_date = user["create_date"]
        self.discoverable = user["discoverable"]
        self._distance_filter = user["distance_filter"]
        self.email = user["email"]
        self.gender = user["gender"]
        self.photo_optimizer_enabled = user["photo_optimizer_enabled"]
        self.ping_time = user["ping_time"]
        self.show_gender_on_profile = user["show_gender_on_profile"]
        self.can_create_squad = user["can_create_squad"]
        if "title" in user["jobs"]:
            self.job_title = user["jobs"]["title"]["name"]
        if "company" in user["jobs"]:
            self.company = user["jobs"]["company"]["name"]
        if "schools" in user:
            self.school = user["schools"]["name"]
        if "city" in user:
            self.city = user["city"]["name"]

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
        self.job_title = title
        self.company = company

    def update_interests(self, **kwargs):
        self._http.post("/v2/profile", {"user": {"user_interests": {"selected_interests": kwargs}}})

    def change_bio(self, bio: str):
        self._http.post("/v2/profile", {"user": {"bio": bio}})

    def change_gender(self, gender: int, show_gender: bool):
        self._http.post("/v2/profile",
                        {"user": {"show_gender_on_profile": show_gender, "gender": gender}})

    def change_sexual_orientation(self, show_orientation, **kwargs):
        self._http.post("/v2/profile",
                        {"user": {"show_orientation_on_profile": show_orientation,
                                  "sexual_orientations": kwargs}})

    def change_school(self, name: str, school_id: str):
        self._http.post("/v2/profile/school",
                        {"schools": {"displayed": True, "name": name, "school_id": school_id}})
        self.school = name

    def reset_school(self):
        self._http.post("/v2/profile/school", {"schools": {}})

    def change_city(self, **kwargs):
        self._http.post("/v2/profile/city", kwargs)
        self.city = kwargs.get("name")

    def reset_city(self):
        self._http.delete("/v2/profile/city")

    def passport_to_location(self, lat, long):
        self._http.post("/passport/user/travel", {"lat": lat, "long": long})

    def reset_passport(self):
        self._http.post("/passport/user/reset")

    def change_location(self, lat, long):
        self._http.post("/user/ping", {"lat": lat, "long": long})

    def like_count(self) -> int:
        return self._http.get("/v2/fast-match/count").json()["data"]["count"]

    def fast_match_preview_urls(self) -> Tuple[str, ...]:
        pass
