import json
import os

class Config:
    def __init__(self, filename="config.json"):
        if not os.path.exists(filename):
            raise FileNotFoundError("config.json introuvable")

        with open(filename, "r") as f:
            self.data = json.load(f)

    def get(self, path, default=None):
        """
        Exemple : get("camera.width")
        """
        keys = path.split(".")
        value = self.data

        for k in keys:
            if k in value:
                value = value[k]
            else:
                return default

        return value
