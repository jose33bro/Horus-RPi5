import numpy as np
import cv2

class CalibrationAI:
    def auto_calibrate(self, frame):
        if frame is None:
            return None

        h, w = frame.shape[:2]

        # Prétraitement
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)              # normalisation lumière
        blur = cv2.GaussianBlur(gray, (9, 9), 2)   # flou pour stabiliser Hough

        # Détection du plateau
        circles = cv2.HoughCircles(
            blur,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=200,
            param1=80,
            param2=30,
            minRadius=50,
            maxRadius=350
        )

        # Valeurs par défaut
        cx = w / 2
        cy = h / 2
        confidence = 0.60

        if circles is not None:
            circles = np.uint16(np.around(circles))
            cx, cy, r = circles[0][0]
            confidence = 0.90

        return {
            "cx": float(cx),
            "cy": float(cy),
            "focal": float(max(w, h)),   # placeholder acceptable
            "confidence": confidence
        }
