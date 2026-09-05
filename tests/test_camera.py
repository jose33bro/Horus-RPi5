"""Tests unitaires pour Camera (ouverture, warmup, exposition/gain/WB, fermeture)."""
import json

import pytest

from horus.engine.camera import Camera


class FakeCap:
    def __init__(self):
        self.opened = True
        self.props = {}
        self.read_count = 0
        self.released = False

    def isOpened(self):
        return self.opened

    def set(self, prop, value):
        self.props[prop] = value
        return True

    def read(self):
        self.read_count += 1
        return True, "frame"

    def release(self):
        self.released = True


@pytest.fixture
def camera(monkeypatch, tmp_path):
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({
        "camera": {
            "index": 0, "width": 640, "height": 480,
            "exposure": -5, "gain": 10, "white_balance": 4500,
            "warmup_frames": 3
        }
    }))

    from horus.utils.config import Config
    cfg = Config(str(cfg_path))
    monkeypatch.setattr("horus.engine.camera.Config", lambda: cfg)

    cam = Camera()
    fake_cap = FakeCap()
    monkeypatch.setattr(
        "horus.engine.camera.cv2.VideoCapture", lambda *a, **k: fake_cap
    )
    cam._fake_cap = fake_cap
    return cam


def test_open_applies_exposure_gain_white_balance_and_warms_up(camera):
    import cv2

    camera.open()

    fake_cap = camera._fake_cap
    assert fake_cap.props[cv2.CAP_PROP_EXPOSURE] == -5
    assert fake_cap.props[cv2.CAP_PROP_GAIN] == 10
    assert fake_cap.props[cv2.CAP_PROP_WB_TEMPERATURE] == 4500
    # 3 images de warmup doivent avoir été lues et ignorées.
    assert fake_cap.read_count == 3


def test_close_releases_capture(camera):
    camera.open()
    camera.close()
    assert camera._fake_cap.released is True
    assert camera.cap is None
