from io import BytesIO
from pathlib import Path
from collections import namedtuple

import requests

img = namedtuple("img", ["url", "hash"])


class SMMS(object):
    root: str = "https://sm.ms/api/v2/"

    def __init__(self, token: str):
        self.header = {"Authorization": token}

    def upload(self, file: Path | str | BytesIO, name: str | None = None) -> img:
        if isinstance(file, str) or isinstance(file, Path):
            files = {"smfile": open(file, "rb")}
        else:
            files = {"smfile": (name, file.getvalue())}
        res = requests.post(self.root + "upload", files=files, headers=self.header)
        res = res.json()
        if res["success"]:
            return img(res["data"]["url"], res["data"]["hash"])
        elif res["code"] == "image_repeated":
            url = res["images"]
            return img(url, self.get_hash_by_url(url))
        else:
            raise ImageUploadError(res["message"])

    def history(self, page: int = 1):
        res = requests.get(
            self.root + f"upload_history?page={page}", headers=self.header
        ).json()
        if res["success"]:
            return res["data"]
        else:
            raise ImageUploadError(res["message"])

    def get_hash_by_url(self, url: str, page: int = 1) -> None:
        item = next((i for i in self.history(page) if i["url"] == url), None)
        if item:
            return item["hash"]
        else:
            raise ImageUploadError("Hash not found by this url.")

    def delete(
        self, url: str | None = None, hash: str | None = None, page: int = 1
    ) -> None:
        if url:
            hash = self.get_hash_by_url(url, page)
        if hash:
            res = requests.get(self.root + "delete/" + hash, headers=self.header).json()
            if not res["success"]:
                raise ImageUploadError(res["message"])
            return
        raise ValueError("Either 'url' or 'hash' must be provided.")


class ImageUploadError(Exception):
    pass
