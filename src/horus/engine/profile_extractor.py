import cv2
import numpy as np
from horus.utils.config import Config


class ProfileExtractor:
    def __init__(self, threshold=None):
        if threshold is None:
            threshold = Config().get("laser.threshold", 200)
        self.threshold = threshold

    def extract_profile(self, frame):
        """
        Détecte la ligne laser et retourne les points (x, y) du profil.

        Accepte aussi bien une image couleur (BGR/BGRA) qu'un masque déjà
        en niveaux de gris/single-channel (ex : sortie de LaserAI.detect()).
        """
        if frame is None:
            return []

        if frame.ndim == 2:
            # Masque single-channel : aucune conversion nécessaire.
            gray = frame
        elif frame.shape[2] == 1:
            gray = frame[:, :, 0]
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Seuillage pour isoler le laser
        _, mask = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY)

        points = cv2.findNonZero(mask)
        if points is None:
            return []

        # Option : filtrer pour garder un point par ligne (plus lumineux)
        profile = {}
        for p in points:
            # cv2.findNonZero renvoie un tableau de forme (N, 1, 2) sur
            # certaines versions d'OpenCV et (N, 2) sur d'autres : on
            # aplatit chaque point pour rester compatible avec les deux.
            px, py = np.ravel(p)
            x, y = int(px), int(py)
            if y not in profile or x < profile[y][0]:
                profile[y] = (x, y)

        return list(profile.values())
