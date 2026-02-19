import numpy as np
import cv2

class PointCloudAI:
    def clean(self, points):
        if points is None or len(points) == 0:
            return points

        # Suppression des points aberrants
        mean = np.mean(points, axis=0)
        dist = np.linalg.norm(points - mean, axis=1)
        threshold = np.mean(dist) + 2 * np.std(dist)
        filtered = points[dist < threshold]

        # Lissage
        if len(filtered) > 10:
            filtered = cv2.GaussianBlur(filtered, (5, 5), 0)

        return filtered

    def interpolate(self, points):
        if points is None or len(points) < 5:
            return points

        # Interpolation simple
        x = points[:, 0]
        y = points[:, 1]
        z = points[:, 2]

        z_interp = cv2.GaussianBlur(z.reshape(-1, 1), (5, 5), 0).flatten()

        return np.column_stack((x, y, z_interp))
