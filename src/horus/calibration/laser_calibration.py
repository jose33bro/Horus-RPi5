import cv2
import numpy as np
from horus.utils.calibration_store import CalibrationStore


class LaserCalibration:
    def __init__(self):
        self.left_laser_plane = None
        self.right_laser_plane = None

    def detect_laser_line(self, frame, threshold=200):
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
        mask = self.detect_laser_line(frame)
        self.left_laser_plane = self.compute_laser_plane(mask)
        return self.left_laser_plane

    def calibrate_right_laser(self, frame):
        mask = self.detect_laser_line(frame)
        self.right_laser_plane = self.compute_laser_plane(mask)
        return self.right_laser_plane
