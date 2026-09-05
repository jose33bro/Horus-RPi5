"""Tests unitaires pour ScanEngine (run_scan_yield / stop / nettoyage)."""
import json

import numpy as np
import pytest

from horus.engine.scan import ScanEngine


class FakeCamera:
    def __init__(self, frames):
        self.frames = list(frames)
        self.opened = False
        self.closed = False
        self.background_subtraction = False

    def open(self):
        self.opened = True

    def read(self):
        if not self.frames:
            raise RuntimeError("no more frames")
        return self.frames.pop(0)

    def close(self):
        self.closed = True


class FakeGRBL:
    def __init__(self):
        self.connected = False
        self.disconnected = False
        self.laser_calls = []
        self.rotations = []

    def connect(self):
        self.connected = True

    def set_laser(self, left=False, right=False):
        self.laser_calls.append((left, right))

    def rotate_relative(self, delta):
        self.rotations.append(delta)

    def disconnect(self):
        self.disconnected = True


class FakeCalibAI:
    def auto_calibrate(self, frame):
        return {"cx": 0, "cy": 0}


class FakePCAI:
    def clean(self, points):
        return points

    def interpolate(self, points):
        return points


@pytest.fixture
def engine(monkeypatch, tmp_path):
    frame = np.zeros((10, 10, 3), dtype=np.uint8)
    frames = [frame.copy() for _ in range(5)]

    eng = ScanEngine.__new__(ScanEngine)
    import threading
    eng._stop_event = threading.Event()
    eng.camera = FakeCamera(frames)
    eng.grbl = FakeGRBL()
    eng.calib_ai = FakeCalibAI()
    eng.pc_ai = FakePCAI()

    from horus.engine.ai_laser import LaserAI
    from horus.engine.profile_extractor import ProfileExtractor
    from horus.engine.reconstruction import Reconstruction3D

    eng.laser_ai = LaserAI()
    eng.extractor = ProfileExtractor(threshold=200)
    eng.reconstruction = Reconstruction3D()
    eng.steps = 3
    eng.step_angle = 10
    eng.output_file = str(tmp_path / "scan.ply")
    return eng


def test_run_scan_yield_cleans_up_hardware_on_success(engine):
    results = list(engine.run_scan_yield())

    assert engine.camera.opened is True
    assert engine.camera.closed is True
    assert engine.grbl.connected is True
    assert engine.grbl.disconnected is True
    # Le laser doit être explicitement coupé à la fin.
    assert engine.grbl.laser_calls[-1] == (False, False)
    # 3 étapes + le message final d'export.
    assert len(results) == 4


def test_run_scan_yield_cleans_up_hardware_on_capture_error():
    eng = ScanEngine.__new__(ScanEngine)
    import threading
    eng._stop_event = threading.Event()

    class RaisingCamera(FakeCamera):
        def read(self):
            raise RuntimeError("boom")

    eng.camera = RaisingCamera([])
    eng.grbl = FakeGRBL()
    eng.calib_ai = FakeCalibAI()
    eng.pc_ai = FakePCAI()

    from horus.engine.ai_laser import LaserAI
    from horus.engine.profile_extractor import ProfileExtractor
    from horus.engine.reconstruction import Reconstruction3D

    eng.laser_ai = LaserAI()
    eng.extractor = ProfileExtractor(threshold=200)
    eng.reconstruction = Reconstruction3D()
    eng.steps = 3
    eng.step_angle = 10
    eng.output_file = "scan.ply"

    with pytest.raises(RuntimeError):
        list(eng.run_scan_yield())

    # Même en cas d'erreur avant la première capture, le matériel doit être
    # nettoyé (laser éteint, caméra/GRBL fermés).
    assert eng.camera.closed is True
    assert eng.grbl.disconnected is True


def test_stop_interrupts_scan_between_steps(engine):
    gen = engine.run_scan_yield()
    next(gen)  # première étape

    engine.stop()

    results = list(gen)
    # Le générateur doit s'arrêter rapidement après stop() sans lever
    # d'exception, tout en nettoyant le matériel.
    assert engine.camera.closed is True
    assert engine.grbl.disconnected is True
