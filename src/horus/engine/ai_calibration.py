import numpy as np
import cv2

class CalibrationAI:
    def auto_calibrate(self, frame):
        if frame is None:
            return None

        h, w = frame.shape[:2]

        # Détection du plateau (simple)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 160)
        circles = cv2.HoughCircles(
            edges, cv2.HOUGH_GRADIENT, 1, 200,
            param1=50, param2=30, minRadius=50, maxRadius=300
        )

        cx = w / 2
        cy = h / 2

        if circles is not None:
            circles = np.uint16(np.around(circles))
            cx, cy, r = circles[0][0]

        return {
            "cx": float(cx),
            "cy": float(cy),
            "focal": float(max(w, h)),
            "confidence": 0.85 if circles is not None else 0.60
        }
