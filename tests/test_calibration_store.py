"""Tests unitaires pour CalibrationStore (persistance des plans laser)."""
import json

from horus.utils.calibration_store import CalibrationStore


def test_store_exposes_left_and_right_plane_attributes(tmp_path, monkeypatch):
    # CalibrationStore résout son chemin relatif à la racine du projet ; on
    # utilise donc un nom de fichier absolu pour rester isolé dans tmp_path.
    store = CalibrationStore(filename=str(tmp_path / "calibration.json"))

    assert hasattr(store, "left_plane")
    assert hasattr(store, "right_plane")
    assert store.left_plane is None
    assert store.right_plane is None


def test_save_updates_in_memory_attributes_and_file(tmp_path):
    path = tmp_path / "calibration.json"
    store = CalibrationStore(filename=str(path))

    store.save((1.0, 2.0, 3.0, 4.0), (5.0, 6.0, 7.0, 8.0))

    assert store.left_plane == (1.0, 2.0, 3.0, 4.0)
    assert store.right_plane == (5.0, 6.0, 7.0, 8.0)

    with open(path) as f:
        data = json.load(f)
    assert data["left_plane"] == [1.0, 2.0, 3.0, 4.0]
    assert data["right_plane"] == [5.0, 6.0, 7.0, 8.0]


def test_load_after_save_round_trips(tmp_path):
    path = tmp_path / "calibration.json"
    store = CalibrationStore(filename=str(path))
    store.save([1, 2, 3, 4], None)

    reloaded = CalibrationStore(filename=str(path))
    assert reloaded.left_plane == [1, 2, 3, 4]
    assert reloaded.right_plane is None
