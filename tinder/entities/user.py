from datetime import datetime
from typing import Tuple

from tinder.entities.entity import Entity
from tinder.http import Http
from tinder.entities.spotify import TopArtist, Track
from tinder.entities.instagram import InstagramInfo


class User(Entity):
    __slots__ = [
        "name",
        "age",
        "bio",
        "ping_time",
        "gender",
        "show_gender_on_profile",
        "_distance",
        "is_travelling",
        "is_tinder_u",
        "interests",
        "badges",
        "photos",
        "spotify_top_artists",
        "theme_track",
        "instagram_info",
        "job_title",
        "company",
        "school",
        "city"
    ]

    def __init__(self, http: Http, user: dict):
        super().__init__(http, user["_id"])
        self.name = user["name"].strip()
        self.age = datetime.now().year - int(user["birth_date"][:4])
        self.bio = user["bio"].strip()
        self.ping_time = user["ping_time"]
        self.gender = user["gender"]
        self.show_gender_on_profile = user["show_gender_on_profile"]
        self._distance = user["distance_mi"]
        self.is_travelling = user["is_travelling"]
        self.is_tinder_u = user["is_tinder_u"]

        interests = list()
        if "user_interests" in user:
            for interest in user["user_interests"]["selected_interests"]:
                interests.append(interest["name"])
        self.interests = tuple(interests)

        badges = list()
        for badge in user["badges"]:
            badges.append(badge["type"])
        self.badges = tuple(badges)

        photos = list()
        for photo in user["photos"]:
            photos.append(photo["url"])
        self.photos = tuple(photos)

        spotify_top_artists = list()
        if "spotify_top_artists" in user:
            for artist in user["spotify_top_artists"]:
                spotify_top_artists.append(TopArtist(artist))
        self.spotify_top_artists: Tuple[TopArtist, ...] = tuple(spotify_top_artists)

        if "spotify_theme_track" in user:
            self.theme_track: Track = Track(user["spotify_theme_track"])

        if "instagram" in user:
            self.instagram_info: InstagramInfo = InstagramInfo(user["instagram"])

        if "title" in user["jobs"]:
            self.job_title = user["jobs"]["title"]["name"]
        if "company" in user["jobs"]:
            self.company = user["jobs"]["company"]["name"]
        if "schools" in user:
            self.school = user["schools"]["name"]
        if "city" in user:
            self.city = user["city"]["name"]

    def distance_mi(self):
        return self._distance

    def distance_km(self):
        return self._distance * 1.609344

    def like(self):
        route = "/like/{}".format(self.entity_id)
        self._http.get(route)

    def dislike(self):
        route = "/pass/{}".format(self.entity_id)
        self._http.get(route)

    def superlike(self):
        route = "/like/{}/super".format(self.entity_id)
        self._http.post(route)
