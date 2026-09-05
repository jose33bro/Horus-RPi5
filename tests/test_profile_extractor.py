"""Tests unitaires pour ProfileExtractor (extraction du profil laser)."""
import numpy as np
import pytest

from horus.engine.profile_extractor import ProfileExtractor


def _make_single_channel_mask():
    mask = np.zeros((10, 10), dtype=np.uint8)
    mask[5, 3] = 255
    mask[5, 7] = 255
    return mask


def test_extract_profile_accepts_single_channel_mask():
    """LaserAI.detect() renvoie un masque single-channel (uint8) : il ne doit
    pas déclencher d'erreur cv2.cvtColor(COLOR_BGR2GRAY) qui exige 3/4 canaux."""
    extractor = ProfileExtractor(threshold=127)
    mask = _make_single_channel_mask()

    profile = extractor.extract_profile(mask)

    assert profile != []
    xs = sorted(p[0] for p in profile)
    assert xs == [3]  # le point le plus à gauche de la ligne y=5 est gardé


def test_extract_profile_accepts_bgr_frame():
    frame = np.zeros((10, 10, 3), dtype=np.uint8)
    frame[5, 3] = (255, 255, 255)

    extractor = ProfileExtractor(threshold=127)
    profile = extractor.extract_profile(frame)

    assert len(profile) == 1
    assert profile[0] == (3, 5)


def test_extract_profile_none_frame_returns_empty_list():
    extractor = ProfileExtractor(threshold=127)
    assert extractor.extract_profile(None) == []


def test_extract_profile_uses_configured_threshold(tmp_path, monkeypatch):
    import json
    from horus.utils.config import Config

    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"laser": {"threshold": 50}}))

    cfg = Config(str(cfg_path))
    monkeypatch.setattr("horus.engine.profile_extractor.Config", lambda: cfg)

    extractor = ProfileExtractor()
    assert extractor.threshold == 50
