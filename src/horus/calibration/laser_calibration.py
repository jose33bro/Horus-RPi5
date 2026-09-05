import cv2
import numpy as np
from horus.utils.calibration_store import CalibrationStore
from horus.utils.config import Config


class LaserCalibration:
    def __init__(self):
        self.left_laser_plane = None
        self.right_laser_plane = None
        self.store = CalibrationStore()
        self.left_laser_plane, self.right_laser_plane = self.store.load()
        self.threshold = Config().get("laser.threshold", 200)

    def detect_laser_line(self, frame, threshold=None):
        if threshold is None:
            threshold = self.threshold
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        mask = cv2.medianBlur(mask, 5)
        return mask

    def compute_laser_plane(self, mask):
        points = cv2.findNonZero(mask)
        if points is None or len(points) < 10:
            return None

        pts = points.reshape(-1, 2)
        [vx, vy, x0, y0] = cv2.fitLine(pts, cv2.DIST_L2, 0, 0.01, 0.01)
        return (vx, vy, x0, y0)

    def calibrate_left_laser(self, frame):
        """Calibre le laser gauche et retourne (plan, masque détecté)."""
        mask = self.detect_laser_line(frame)
        self.left_laser_plane = self.compute_laser_plane(mask)
        self.store.save(self.left_laser_plane, self.right_laser_plane)
        return self.left_laser_plane, mask

    def calibrate_right_laser(self, frame):
        """Calibre le laser droit et retourne (plan, masque détecté)."""
        mask = self.detect_laser_line(frame)
        self.right_laser_plane = self.compute_laser_plane(mask)
        self.store.save(self.left_laser_plane, self.right_laser_plane)
        return self.right_laser_plane, mask

