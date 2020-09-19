from datetime import datetime
from typing import Tuple

from tinder.entities.entity import Entity
from tinder.http import Http
from tinder.entities.spotify import TopArtist, Track
from tinder.entities.instagram import InstagramInfo


class User(Entity):
    def __init__(self, http: Http, user: dict):
        super().__init__(http, user["_id"])
        self.name = user["name"].strip()
        self.age = datetime.now().year - int(user["birth_date"][:4])
        self.bio = user["bio"].strip()
        self._distance = user["distance_mi"]

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

        if "photos" in user["instagram"]:
            self.instagram_info: InstagramInfo = InstagramInfo(user["instagram"])

    def distance_mi(self):
        return self._distance

    def distance_km(self):
        return self._distance * 1.609344

    def like(self):
        route = "/like/{}".format(self.entity_id)
        self._http.get(route).json()

    def dislike(self):
        route = "/pass/{}".format(self.entity_id)
        self._http.get(route)

    def superlike(self):
        route = "/like/{}/super".format(self.entity_id)
        self._http.post(route)
