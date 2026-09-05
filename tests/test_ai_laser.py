"""Tests unitaires pour LaserAI (détection laser, canal masque, config HSV)."""
import json
import numpy as np
import pytest

from horus.engine.ai_laser import LaserAI, DEFAULT_HSV_RANGES


def test_detect_returns_single_channel_mask_without_model():
    ai = LaserAI(tflite_path=None)
    frame = np.zeros((20, 20, 3), dtype=np.uint8)
    frame[10, 10] = (0, 0, 255)  # rouge en BGR -> détectable par le fallback HSV

    mask = ai.detect(frame)

    assert mask is not None
    assert mask.ndim == 2  # masque single-channel, pas BGR
    assert mask.dtype == np.uint8


def test_missing_tflite_model_falls_back_to_hsv(tmp_path):
    ai = LaserAI(tflite_path=str(tmp_path / "does-not-exist.tflite"))
    assert ai.model is None
    assert ai.model_loaded is False


def test_detect_none_frame_returns_none():
    ai = LaserAI()
    assert ai.detect(None) is None


def test_hsv_ranges_from_config_are_used():
    custom_ranges = [[[40, 40, 40], [80, 255, 255]]]
    ai = LaserAI(hsv_ranges=custom_ranges)
    assert ai.hsv_ranges == [((40, 40, 40), (80, 255, 255))]


def test_invalid_hsv_ranges_fallback_to_default():
    ai = LaserAI(hsv_ranges="not-a-valid-range")
    assert ai.hsv_ranges == DEFAULT_HSV_RANGES


def test_no_hsv_ranges_uses_default():
    ai = LaserAI(hsv_ranges=None, tflite_path=None)
    # hsv_ranges=None triggers config lookup which returns [] by default (no config laser.hsv_ranges key found on cwd)
    assert ai.hsv_ranges  # non-empty list of ranges
