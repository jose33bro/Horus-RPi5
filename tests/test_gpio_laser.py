"""Tests unitaires pour GPIOLaserController (contrôle laser via GPIO, no-op sans matériel)."""
import json

from horus.engine.gpio_laser import GPIOLaserController


def test_gpio_disabled_by_default_is_noop(tmp_path, monkeypatch):
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({"laser": {"gpio": {"enabled": False}}}))

    from horus.utils.config import Config
    cfg = Config(str(cfg_path))
    monkeypatch.setattr("horus.engine.gpio_laser.Config", lambda: cfg)

    ctrl = GPIOLaserController()
    assert ctrl.enabled is False
    # Ne doit lever aucune exception même sans matériel GPIO.
    ctrl.set_laser(left=True)
    ctrl.close()


def test_gpio_enabled_reads_pins_from_config(tmp_path, monkeypatch):
    cfg_path = tmp_path / "config.json"
    cfg_path.write_text(json.dumps({
        "laser": {"gpio": {"enabled": True, "left_pin": 5, "right_pin": 6}}
    }))

    from horus.utils.config import Config
    cfg = Config(str(cfg_path))
    monkeypatch.setattr("horus.engine.gpio_laser.Config", lambda: cfg)

    ctrl = GPIOLaserController()
    assert ctrl.left_pin == 5
    assert ctrl.right_pin == 6
