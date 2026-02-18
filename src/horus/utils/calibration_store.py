import json
import os

class CalibrationStore:
    def __init__(self, filename="calibration.json"):
        self.filename = filename

    def save(self, left_plane, right_plane):
        data = {
            "left_plane": list(left_plane) if left_plane else None,
            "right_plane": list(right_plane) if right_plane else None
        }

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        if not os.path.exists(self.filename):
            return None, None

        with open(self.filename, "r") as f:
            data = json.load(f)

        return data.get("left_plane"), data.get("right_plane")
