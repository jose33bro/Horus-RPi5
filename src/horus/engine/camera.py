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
