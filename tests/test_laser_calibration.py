"""Tests unitaires pour LaserCalibration (retour (plane, mask), sauvegarde)."""
import json

import numpy as np
import pytest

from horus.calibration.laser_calibration import LaserCalibration


@pytest.fixture
def calib(tmp_path):
    from horus.utils.calibration_store import CalibrationStore

    store = CalibrationStore(filename=str(tmp_path / "calibration.json"))

    c = LaserCalibration.__new__(LaserCalibration)
    c.left_laser_plane = None
    c.right_laser_plane = None
    c.store = store
    c.threshold = 127
    return c


def _frame_with_vertical_line():
    frame = np.zeros((50, 50, 3), dtype=np.uint8)
    # Ligne large (5 px) : une ligne laser réelle a une certaine épaisseur et
    # doit survivre au filtre médian appliqué par detect_laser_line().
    frame[:, 23:28] = (255, 255, 255)
    return frame


def test_calibrate_left_laser_returns_plane_and_mask(calib):
    frame = _frame_with_vertical_line()

    result = calib.calibrate_left_laser(frame)

    assert isinstance(result, tuple)
    assert len(result) == 2
    plane, mask = result
    assert plane is not None
    assert mask.ndim == 2


def test_calibrate_right_laser_does_not_clobber_left_plane(calib):
    frame = _frame_with_vertical_line()

    calib.calibrate_left_laser(frame)
    left_after_left = calib.store.left_plane
    assert left_after_left is not None

    calib.calibrate_right_laser(frame)

    # La calibration du laser droit ne doit pas effacer le plan gauche
    # précédemment sauvegardé.
    assert calib.store.left_plane == left_after_left
    assert calib.store.right_plane is not None
