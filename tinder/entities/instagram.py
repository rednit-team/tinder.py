from typing import Tuple


class InstagramInfo:
    __slots__ = ["last_fetch_time", "completed_initial_fetch", "media_count", "photos"]

    def __init__(self, instagram: dict):
        self.last_fetch_time = instagram["last_fetch_time"]
        self.completed_initial_fetch = instagram["completed_initial_fetch"]
        self.media_count = instagram["media_count"]

        photos = list()
        if "photos" in instagram:
            for photo in instagram["photos"]:
                photos.append(InstagramPhoto(photo))
        self.photos: Tuple[InstagramPhoto, ...] = tuple(photos)


class InstagramPhoto:
    __slots__ = ["image", "thumbnail", "ts"]

    def __init__(self, photo: dict):
        self.image = photo["image"]
        self.thumbnail = photo["thumbnail"]
        self.ts = photo["ts"]
