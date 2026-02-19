import numpy as np
from scipy.ndimage import gaussian_filter1d

class PointCloudAI:
    def clean(self, points):
        """
        Nettoyage du nuage de points :
        - suppression des outliers globaux
        - lissage léger des coordonnées
        """
        if points is None or len(points) == 0:
            return points

        # Suppression des points aberrants (distance au centre)
        mean = np.mean(points, axis=0)
        dist = np.linalg.norm(points - mean, axis=1)
        threshold = np.mean(dist) + 2 * np.std(dist)
        filtered = points[dist < threshold]

        if len(filtered) < 5:
            return filtered

        # Lissage 1D sur chaque axe
        x = gaussian_filter1d(filtered[:, 0], sigma=1)
        y = gaussian_filter1d(filtered[:, 1], sigma=1)
        z = gaussian_filter1d(filtered[:, 2], sigma=1)

        return np.column_stack((x, y, z))

    def interpolate(self, points):
        """
        Interpolation simple du nuage :
        - lissage supplémentaire de Z
        """
        if points is None or len(points) < 5:
            return points

        x = points[:, 0]
        y = points[:, 1]
        z = points[:, 2]

        # Lissage plus fort sur Z
        z_interp = gaussian_filter1d(z, sigma=2)

        return np.column_stack((x, y, z_interp))
