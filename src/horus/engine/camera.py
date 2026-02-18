import cv2

class Camera:
    from horus.utils.config import Config

class Camera:
    def __init__(self):
        cfg = Config()
        self.index = cfg.get("camera.index")
        self.width = cfg.get("camera.width")
        self.height = cfg.get("camera.height")

        self.index = index
        self.width = width
        self.height = height
        self.cap = None

    def open(self):
        self.cap = cv2.VideoCapture(self.index, cv2.CAP_V4L2)

        if not self.cap.isOpened():
            raise RuntimeError(f"Impossible d'ouvrir la caméra index {self.index}")

        # Configuration de la résolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def read(self):
        if self.cap is None:
            raise RuntimeError("La caméra n'est pas ouverte")

        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Erreur de capture : aucune image reçue")

        return frame

    def close(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None
