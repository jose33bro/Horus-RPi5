import cv2
import numpy as np

class ProfileExtractor:
    def __init__(self, threshold=200):
        self.threshold = threshold

    def extract_profile(self, frame):
        """
        Détecte la ligne laser et retourne les points (x, y) du profil.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Seuillage pour isoler le laser
        _, mask = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY)

        points = cv2.findNonZero(mask)
        if points is None:
            return []

        # Option : filtrer pour garder un point par ligne (plus lumineux)
        profile = {}
        for p in points:
            x, y = int(p[0][0]), int(p[0][1])
            if y not in profile or x < profile[y][0]:
                profile[y] = (x, y)

        return list(profile.values())
