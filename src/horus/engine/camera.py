import cv2
from horus.utils.config import Config
from horus.utils.logger import logger

class Camera:
    def __init__(self):
        cfg = Config()

        # Lecture de la config
        self.index = cfg.get("camera.index", 0)
        self.width = cfg.get("camera.width", 1280)
        self.height = cfg.get("camera.height", 720)
        self.exposure = cfg.get("camera.exposure", None)
        self.gain = cfg.get("camera.gain", None)
        self.white_balance = cfg.get("camera.white_balance", None)
        self.warmup_frames = cfg.get("camera.warmup_frames", 5)
        self.background_subtraction = cfg.get("camera.background_subtraction", False)

        self.cap = None

    def open(self):
        logger.info(f"Ouverture de la caméra index={self.index}")

        # Ouverture V4L2 (Raspberry Pi 5)
        self.cap = cv2.VideoCapture(self.index, cv2.CAP_V4L2)

        if not self.cap.isOpened():
            logger.error(f"Impossible d'ouvrir la caméra index {self.index}")
            raise RuntimeError(f"Impossible d'ouvrir la caméra index {self.index}")

        # Configuration de la résolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        # Exposition / gain / balance des blancs manuels (meilleur contraste laser)
        if self.exposure is not None:
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)  # mode manuel (V4L2 : 1)
            self.cap.set(cv2.CAP_PROP_EXPOSURE, self.exposure)

        if self.gain is not None:
            self.cap.set(cv2.CAP_PROP_GAIN, self.gain)

        if self.white_balance is not None:
            self.cap.set(cv2.CAP_PROP_AUTO_WB, 0)
            self.cap.set(cv2.CAP_PROP_WB_TEMPERATURE, self.white_balance)

        self._warmup()

    def _warmup(self):
        """Capture et ignore quelques images pour laisser la caméra se stabiliser
        (auto-exposition/gain matériel avant de figer les réglages manuels)."""
        for _ in range(self.warmup_frames):
            try:
                self.cap.read()
            except Exception:
                break

    def capture_background(self):
        """Capture une image de référence (laser éteint) pour la soustraction de fond."""
        return self.read()

    def read(self):
        if self.cap is None:
            raise RuntimeError("La caméra n'est pas ouverte")

        ret, frame = self.cap.read()
        if not ret:
            logger.error("Erreur de capture : aucune image reçue")
            raise RuntimeError("Erreur de capture : aucune image reçue")

        return frame

    def close(self):
        if self.cap is not None:
            logger.info("Fermeture de la caméra")
            self.cap.release()
            self.cap = None
