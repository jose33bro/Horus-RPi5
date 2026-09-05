"""
Contrôle des lasers via GPIO (Raspberry Pi 5), en complément du contrôle
GRBL (M3/M5). Utilise gpiozero, qui repose sur lgpio/pigpio pour le RPi 5.

Ce module est optionnel : si gpiozero n'est pas installé ou si le code
tourne hors Raspberry Pi (pas de GPIO physique), toutes les opérations
deviennent des no-op et sont journalisées, sans lever d'exception.
"""

from horus.utils.config import Config
from horus.utils.logger import logger

try:
    from gpiozero import LED
    GPIOZERO_AVAILABLE = True
except Exception:
    LED = None
    GPIOZERO_AVAILABLE = False


class GPIOLaserController:
    """Pilote les lasers gauche/droit directement via des GPIO BCM."""

    def __init__(self, left_pin=None, right_pin=None, active_high=None):
        cfg = Config()
        gpio_cfg = cfg.get("laser.gpio", {}) or {}

        self.enabled = bool(gpio_cfg.get("enabled", False))
        self.left_pin = left_pin if left_pin is not None else gpio_cfg.get("left_pin", 17)
        self.right_pin = right_pin if right_pin is not None else gpio_cfg.get("right_pin", 27)
        self.active_high = (
            active_high if active_high is not None else gpio_cfg.get("active_high", True)
        )

        self._left = None
        self._right = None

        if self.enabled and GPIOZERO_AVAILABLE:
            try:
                self._left = LED(self.left_pin, active_high=self.active_high)
                self._right = LED(self.right_pin, active_high=self.active_high)
                logger.info(
                    f"GPIO laser initialisé (gauche=BCM{self.left_pin}, "
                    f"droit=BCM{self.right_pin})"
                )
            except Exception as e:
                logger.error(f"Impossible d'initialiser les GPIO laser : {e}")
                self._left = None
                self._right = None
        elif self.enabled and not GPIOZERO_AVAILABLE:
            logger.warning(
                "laser.gpio.enabled=true mais gpiozero n'est pas installé, "
                "le contrôle GPIO du laser est désactivé."
            )

    def set_laser(self, left=False, right=False):
        """Active/désactive les lasers via GPIO. No-op si GPIO indisponible."""
        if self._left is not None:
            self._left.on() if left else self._left.off()
        if self._right is not None:
            self._right.on() if right else self._right.off()

    def close(self):
        for pin in (self._left, self._right):
            if pin is not None:
                try:
                    pin.close()
                except Exception:
                    pass
        self._left = None
        self._right = None
