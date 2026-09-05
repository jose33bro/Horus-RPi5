"""Tests unitaires pour GRBLController (synchronisation des commandes GRBL)."""
import json

import pytest

from horus.engine.grbl_controller import GRBLController


class FakeSerial:
    """Simule un port série GRBL : répond "ok" à chaque commande écrite."""

    def __init__(self, *args, **kwargs):
        self.written = []
        self._responses = [b"ok\n"]

    def reset_input_buffer(self):
        pass

    def reset_output_buffer(self):
        pass

    def write(self, data):
        self.written.append(data)

    def flush(self):
        pass

    def readline(self):
        return self._responses[0]

    def close(self):
        pass


@pytest.fixture
def controller(monkeypatch, tmp_path):
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"grbl": {"port": "/dev/fake", "baudrate": 9600}}))

    from horus.utils.config import Config
    cfg = Config(str(cfg_path))
    monkeypatch.setattr("horus.engine.grbl_controller.Config", lambda: cfg)
    monkeypatch.setattr("horus.engine.gpio_laser.Config", lambda: cfg)

    ctrl = GRBLController()
    fake = FakeSerial()
    monkeypatch.setattr("horus.engine.grbl_controller.time.sleep", lambda s: None)
    monkeypatch.setattr(
        "horus.engine.grbl_controller.serial.Serial", lambda *a, **k: fake
    )
    ctrl.connect()
    ctrl._fake_serial = fake
    return ctrl


def test_rotate_relative_sends_each_command_separately_and_acks(controller):
    fake = controller._fake_serial
    fake.written.clear()  # ignore la commande $X envoyée à la connexion

    controller.rotate_relative(1.8)

    # Chaque commande G-code doit être écrite (et acquittée) séparément,
    # au lieu d'un seul write() combinant G91/G0/G90.
    assert fake.written == [b"G91\n", b"G0 A1.8\n", b"G90\n"]


def test_set_laser_sends_grbl_command(controller):
    fake = controller._fake_serial
    fake.written.clear()

    controller.set_laser(left=True)

    assert fake.written == [b"M3 S128\n"]
